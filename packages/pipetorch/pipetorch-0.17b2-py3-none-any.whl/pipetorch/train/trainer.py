import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import AdamW, Adam, RMSprop, Adadelta, Adagrad, Adamax, LBFGS, SGD, SparseAdam
import timeit
import sys
import copy
import gc
import numpy as np
import math
import hashlib
from pathlib import Path
from pipetorch.evaluate.evaluate import EvaluatorTorch, EvaluatorSK
from torcheval.metrics import *
from pipetorch.helper import run_magic
from torch.optim.lr_scheduler import OneCycleLR, ConstantLR
from pipetorch.train.tuner import *
from pipetorch.train.helper import tqdm_trainer, partial_replace_args, optimizer_to
from torch.nn.parallel.comm import broadcast
from functools import partial
import pandas as pd
import os
from io import StringIO
from collections import Counter
from operator import itemgetter
import warnings
try:
    import torch_xla.core.xla_model as xm
except: pass
    
def to_numpy(arr):
    try:
        return arr.data.cpu().numpy()
    except: pass
    try:
        return arr.to_numpy()
    except: pass
    return arr

def UniformLR(*args, **kwargs):
    class Uniform_Scheduler:
        def step(self):
            pass
    return Uniform_Scheduler()

def onecycle(optimizer, lr, steps):
    return OneCycleLR(optimizer, lr[1], total_steps=steps)

def halt_notebook():
    import IPython
    ip = IPython.get_ipython()
    ip.ask_exit()
    
class ordered_dl:
    def __init__(self, dl):
        self.dl = dl

    def __enter__(self):
        self.oldsampler = self.dl.batch_sampler.sampler
        self.newsampler = torch.utils.data.sampler.SequentialSampler(self.oldsampler.data_source)
        self.dl.batch_sampler.sampler = self.newsampler
        return self.dl

    def __exit__(self, exc_type, exc_value, tb):
        self.dl.batch_sampler.sampler = self.oldsampler
        if exc_type is not None:
            return False

class trainsession:
    def __init__(self, trainer, silence=True, cleanup=True):
        self.trainer = trainer
        self.old_silent = trainer.silent
        self.new_silent = silence
        self.cleanup = cleanup

    def __enter__(self):
        self.trainer.silent = self.new_silent
        return self.trainer

    def __exit__(self, exc_type, exc_value, tb):
        self.trainer.silent = self.old_silent
        if self.cleanup:
            self.trainer.cleanup()

def argmax(y):
    return torch.argmax(y, dim=1)

def identity(x):
    return x

POST_FORWARD = {nn.L1Loss:None, 
                nn.MSELoss:None, 
                nn.CrossEntropyLoss:argmax,
                nn.NLLLoss: argmax, 
                nn.PoissonNLLLoss: argmax, 
                nn.GaussianNLLLoss: argmax, 
                nn.KLDivLoss: argmax, 
                nn.BCELoss: torch.round, 
                nn.BCEWithLogitsLoss: torch.round, 
                nn.HuberLoss: None,
                nn.SmoothL1Loss: None
               }
        
class Trainer:
    """
    A general purpose trainer for PyTorch.
    
    Arguments:
        model: nn.Module
            a PyTorch Module that will be trained
            
        loss: callable
            a PyTorch or custom loss function
            
        *databunch: databunch or a list of iterables (DataLoaders)
            a databunch is an object that has a train_dl, valid_dl,
            and optionally test_dl property. Databunches can be generated
            by DFrame with to_databunch, but you may also pass your own
            object that has at least a train_dl and valid_dl property.
            
            Alternatively, a list of iterables can also be given in the
            order train, test, (valid). When only two dataloaders are provided
            the second will be used both as valid and test. Most often, 
            these iterables are PyTorch DataLoaders that are used to iterate 
            over the datasets for training and validation.
            
        train_dl: iterable (DataLoader)
            when databunch is not used, you can use the named argument to
            assign an iterable or DataLoader used for training
            
        test_dl: iterable (DataLoader)
            when databunch is not used, you can use the named argument to
            assign an iterable or DataLoader used for testing
            
        valid_dl: iterable (DataLoader)
            when databunch is not used, you can use the named argument to
            assign an iterable or DataLoader used for validation
            
        metrics: callable or list of callable (None)
            One or more functions that can be called with (y, y_pred)
            to compute an evaluation metric. This will automatically be
            done during training, for both the train and valid sets.
            Typically, the callable is a function from SKLearn.metrics
            like mean_squared_error or recall_score.
            
        optimizer: PyTorch Optimizer or str (AdamW)
            The PyTorch or custom optimizer CLASS (not an instance!) that is 
            used during training.
            
            You can either provide:
            - an optimizer CLASS from the torch.optim module,
            - a custom optimizer CLASS that obeys the same API, 
            - a partial of an optimizer CLASS with optimization arguments set
            - 'AdamW', 'Adam', 'RMSprop', 'Adadelta', 'Adagrad', 'Adamax', 
              'LBFGS', 'SGD', or 'SparseAdam'
                        
        scheduler: None, OneCycleLR, ConstantLR
            used to adapt the learning rate: 
            - None will use a constant learning rate
            - OneCycleLR will will use a cyclic annealing learning rate
              between an upper and lower bound.
            - ConstantLR will use a linear decaying learning rate between
              an upper bound and lower bound. You can optionally use
              'cycle' when calling 'train' to restart ConstantLR 
              every 'cycle' epochs.
              
        weight_decay: float
            When set, the trainer will attempt to instantiate an optimizer
            with weight_decay set. When the optimizer does not support weight
            decay, it will fail.
            
        betas: float
            When set, the trainer will attempt to instantiate an optimizer
            with betas set. When the optimizer does not support betas it will fail.
            
        random_state: int
            used to set a random state for reproducible results
            
        gpu: bool, int or torch.device
            The device to train on:
                False or -1: cpu
                True: cuda:0, this is probably what you want to train on gpu
                int: cuda:gpu
            Setting the device will automatically move the model and data to
            the given device. Note that the model is not automatically
            transfered back to cpu afterwards.
    
        evaluator: PipeTorch evaluator
            An evaluator that was created by a different trainer or 
            DataFrame, to combine the results of different training
            sessions.
            
        post_forward: func (None)
            For some projects, the loss function requires a different output than
            the metrics that are being used. 

            Example 1: For nn.BCELoss() the target value
            must be a likelihood, while accuracy_score requires a class label. 
            The model returns a likelihood with an nn.Sigmoid() on the ouput layer, 
            but the metrics can only be computed if the likelihood is converted into 
            a predicted label (e.g. torch.round() ). 

            Example 2: nn.CrossEntropyLoss() requires a distribution over the possible labels
            while multi-class evaluation matrics require the predicted class. This is commonly
            computed with torch.argmax(y, dim=1).

            To allow for this behavior, the trainer can use a post_forward fuction inbetween
            loss and metrics. It will attempt to use a post_forward in the following order: 
            - a function passed here
            - a post_forward method that is added to the model
            - infer a post_forward based on the loss function. 

            For inferring a post_forward based on
            the loss function, there is a dictionary in train.POST_FORWARD that covers the 
            most commonly used loss functions.

            If no post_forward is found, and the loss function is unknown, then None is used
            and a warning is printed. Pass post_forward=False to suppress this warning.
            
        annotation: {}
            a dictionary with values that are added to the recorded results of a training. All results
            are always annotated with:
            - model(name as given by the trainer's label), 
            - phase (train, valid or test)
            - epoch
            
            Addionally, you can add values that can help to distinguish several series of experiments 
            that are recorded in the same resultset (actually an Evaluator that holds EvaluatorResults). 
            There are a few reasons to do this: 
            (1) it becomes easier to compare experiments that are recorded in the same resultset and 
            (2) for determining the optimal epoch in a training run (using optimum()),
            the trainer will only consider results with the same annotation.
            
        silent: bool (False)
            Whether this trainer will print messages
            
        halt_notebook: bool (True)
            If True, after a call to train() the model is automatically saved and the notebook is
            halted. This is done automatically to free up resources and because users tend to forget
            to close off their notebooks. Often the process should continue after a call to train(), 
            for instance to run validation or to schedule multiple training sessions to tune hyperparameter.
            In that case, set halt_notebook=False and add a calls to 
            save()/save_trainer() and halt_notebook() in the last_cells.
            
        debug: bool (False)
            stores X, y and y_pred in properties so that they can be inspected
            when an error is thrown.
    """
    def __init__(self, 
                 model, 
                 loss, 
                 train_dl=None,
                 valid_dl=None,
                 test_dl=None,
                 *,
                 db=None,
                 metrics = None, 
                 optimizer='AdamW', 
                 scheduler=None, 
                 weight_decay=None, 
                 betas=None,
                 lr=1e-2,
                 cycle=None,
                 gpu=True,
                 random_state=None, 
                 evaluator=None, 
                 evaluator_class=None,
                 debug=False,
                 silent=False,
                 save_lowest=False, 
                 pbar=None,
                 targetloss=None, 
                 targettrainloss=None, 
                 earlystop=False,
                 post_forward=None,
                 annotation={},
                 validate=True, 
                 test=False,
                 label=None,
                 halt_notebook=True
                ):
        # the amount of epochs in a cycle, 
        # validation is only done at the end of each cycle
        self.loss = loss
        self.random_state = random_state
        self.gpu = gpu
        if db is not None:
            assert train_dl is None, 'You cannot use a databunch with train_dl'
            assert test_dl is None, 'You cannot use a databunch with test_dl'
            assert valid_dl is None, 'You cannot use a databunch with valid_dl'            
            self.databunch = db
        else:
            assert train_dl is not None, 'You must specify train_dl'
            assert valid_dl is not None, 'You must specify valid_dl'
            self.train_dl = train_dl
            self.valid_dl = valid_dl
            self.test_dl = test_dl
        self.model = model
        self._debug = debug
        self.silent = silent
        self._set_post_forward(post_forward, model, loss)
        self.optimizer = optimizer
        self.scheduler = scheduler
        if self.random_state is not None:
            torch.backends.cudnn.deterministic=True
            torch.manual_seed(self.random_state)
        self._commit = {}
        self.epochid = 0
        self.batch = 0
        self.weight_decay = weight_decay
        self.betas = betas
        self.lowest_validloss=None
        self.lowest_validtest_loss=None
        self.lowest_validtest_y=None
        self.lowest_validtest_y_pred=None
        if evaluator is not None:
            assert metrics == None, 'When you assign an evaluator, you cannot assign different metrics to a trainer'
            self._evaluator = evaluator
            self.metrics = evaluator.metrics
        else:
            self.metrics = metrics or []
        if evaluator_class is not None:
            self._evaluator_class = evaluator_class
        self._conf_cycle = cycle
        self._conf_validate = validate
        self._conf_test = test
        self._conf_validate_annotation = annotation
        self.label = label
        self._conf_earlystop = earlystop
        self._conf_save_lowest = save_lowest
        self.targetloss = targetloss
        self.targettrainloss = targettrainloss
        self.lr = lr
        self.pbar = pbar
        self.lead_trainer = None
        self._halt_notebook = halt_notebook
        
    def cotrain(self, 
                 model, 
                 loss, 
                 metrics = None, 
                 optimizer='AdamW', 
                 scheduler=None,
                 weight_decay=None, 
                 betas=None, 
                 gpu=True,
                 random_state=None, 
                 debug=False,
                 silent=True,
                 post_forward=None,
                 lr=1e-2,
                 cycle=None,
                 halt_notebook=False,
                 save_lowest=False, 
                 pbar=None,
                 label=None,
                 annotation=None
                ):
        """
        Create a CoTrainer that will be registered to this Trainer. 
        
        Any call to train() with nothing
        more than epochs and cycle will train the Trainer and all registered CoTrainers 
        simultaneously using the same datafeed and thus being much more efficient on servers with
        a disk I/O bottleneck. The CoTrainer will always share the 
        
        """
        metrics = metrics or self.metrics
        return CoTrainer(self, model, loss, metrics=metrics, optimizer=optimizer,
                        scheduler=scheduler, weight_decay=weight_decay, betas=betas,
                        gpu=gpu, random_state=random_state, 
                        debug=debug, silent=silent,
                        post_forward=post_forward, lr=lr, cycle=cycle, 
                        save_lowest=save_lowest, pbar=pbar, label=label, annotation=annotation)

    @classmethod
    def multi(cls, models, 
                 losses, 
                 db=None,
                 train_dl=None,
                 test_dl=None,
                 valid_dl=None,
                 metrics = None, 
                 optimizers='AdamW', 
                 schedulers=None, 
                 weight_decays=None, 
                 betas=None,
                 lrs=None,
                 cycle=None,
                 gpu=True,
                 random_state=None, 
                 evaluator=None,
                 evaluator_class=None,
                 debug=False,
                 silent=False,
                 save_lowest=False, 
                 pbar=None,
                 targetloss=None, 
                 targettrainloss=None, 
                 earlystop=False,
                 post_forwards=None,
                 annotations={},
                 validate=True, 
                 test=False,
                 labels=None,
                 halt_notebook=True
                ):
        """
        Constructs a Trainer that will train multiple instances simultaneously while traversing the data,
        thus being more efficient.
        
        The arguments model, losses, optimizers, schedulers, betas, lrs, annotations and labels can either 
        have one value or a list of values. 
        The largest list will determine the number of (Co)Trainers that are created.
        If the count of the list does not match that number, it is assumed to be a single value. The parameters
        with single values are replicated so that every trainer will use the same value. One exception is
        that when a model is replicated, a deepcopy is made to ensure that every trainer has their own model.
        
        The first trainer will train the first model with the first pair of settings and will hold the 
        data. The other trainers will be CoTrainer with separate models and settings. The CoTrainer will 
        share the data, evaluator, cycle, pbar, targetloss, targettrainloss, earlystop, debug, validate, 
        test, random_state with the lead trainer. The CoTrainers are always instantiated with GPU=True by default
        since this makes most sense.
        
        Args:
            models: nn.Module or [nn.Module]
            losses: loss function or [ loss function ]
            optimizers: str or [ str ] (None)
            schedulers: str or [ str ] (None)
            weight_decays: float or [ float ]
            betas: (float, float) or [(float, float)]
            lrs: float or [float] or (float, float) or [(float, float)] or [float, float] or [[float, float]]
            labels: str or [str]
            annotations: {} or [{}]
                Since the results are added to a shared resultset, a single annotation dictionary will
                be assigned to the lead trainer and linked to the cotrainers. That way, if the annotations
                of the lead traine are modified, it carries to the cotrainers. In all cases,
                all trainers will register their results with their label as model, which unless specified 
                will contain the trainer number. This allows to distinguish
                results between trainers. If a list of annotation dictionaries is provided, these will be
                used by the trainers in that order.
            post_forwards: callable or [ callable ] (None)
            
        returns: Trainer
            the lead Trainer, with registered CoTrainer(s) tat can be accessed through Trainer.cotrainers.
            Calling train on the Trainer with nothing but a number of epochs and a cycle will train all models
            simultaneously.
        """

        models, losses, optimizers, schedulers, weight_decays, betas, lrs, labels, post_forwards = \
            cls._match_multi(models, losses, optimizers, schedulers, weight_decays, betas, lrs, labels, post_forwards)

        if silent:
            pbar=False
            
        if type(annotations) == dict or annotations is None:
            annotations = [annotations] + [None] * (len(models)-1)

        lead = cls(models[0], losses[0], db=db, train_dl=train_dl, test_dl=test_dl,
                valid_dl=valid_dl, metrics = metrics, optimizer=optimizers[0], scheduler=schedulers[0], 
                weight_decay=weight_decays[0], betas=betas[0], lr=lrs[0], cycle=cycle, 
                gpu=gpu, random_state=random_state, evaluator=evaluator, evaluator_class=evaluator_class,
                debug=debug, silent=silent, save_lowest=save_lowest,
                pbar=pbar, targetloss=targetloss, targettrainloss=targettrainloss, 
                earlystop=earlystop, post_forward=post_forwards[0], annotation=annotations[0],
                validate=validate, test=test, label=labels[0], halt_notebook=halt_notebook)
        
        for i in range(1, len(models)):
            lead.cotrain(models[i], losses[i], 
                optimizer=optimizers[i], scheduler=schedulers[i], 
                weight_decay=weight_decays[i], betas=betas[i], lr=lrs[i],
                gpu=True, random_state=random_state, debug=debug,
                silent=True, save_lowest=save_lowest,
                post_forward=post_forwards[i],
                label=labels[i],
                annotation=annotations[i])
        return lead

    @classmethod
    def _match_multi(cls, *args):
        count = 1
        for a in args:
            if type(a) == list:
                count = max(count, len(a))
        r = []
        for a in args:
            if type(a) == list:
                if len(a) == count:
                    r.append(a)
                    continue
            if isinstance(a, nn.Module):
                rr = [a]
                for i in range(count-1):
                    rr.append(copy.deepcopy(a))
                r.append(rr)
            else:
                r.append([a] * count)
        return r
                
    @classmethod
    def _replicate_param(cls, value, models):
        if type(value) == list or type(value) == tuple:
            assert len(value) == len(models), f'value {value} does not match models {models} in size'
            return value
        return [value] * len(models)
    
    @property
    def _conf_validate_annotation(self):
        return self.__conf_validate_annotation
    
    @_conf_validate_annotation.setter
    def _conf_validate_annotation(self, value):
        self.__conf_validate_annotation = value
        try:
            del self.__validate_annotation
        except: pass
    
    @property
    def label(self):
        if self._label is None:
            return self.model.__class__.__name__
        return self._label
    
    @label.setter
    def label(self, value):
        self._label = value
        try:
            del self.__validate_annotation
        except: pass
    
    @property
    def _validate_annotation(self):
        try:
            return self.__validate_annotation
        except:
            self.__validate_annotation = dict(self._conf_validate_annotation)
            return self.__validate_annotation
            
    def copy(self):
        return Trainer(self.model, 
                       self.loss, 
                       train_dl = self.train_dl,
                       valid_dl = self.valid_dl,
                       test_dl = self.test_dl,
                       db = self.databunch,
                       metrics=self.metrics, 
                       optimizer=self._optimizer_class, 
                       scheduler=self._scheduler_class, 
                       weight_decay=self.weight_decay, 
                       betas=self.betas, 
                       gpu=self.device,
                       random_state=self.random_state, 
                       post_forward=self.post_forward,
                       cycle=self._conf_cycle,
                       evaluator=self.evaluator.clone(),
                       debug=self._debug,
                       silent=self.silent,
                       save_lowest = self._conf_save_lowest,
                       targetloss=self.targetloss, 
                       targettrainloss=self.targettrainloss, 
                       earlystop=self._conf_earlystop,
                       annotation=self._conf_validate_annotation,
                       halt_notebook=self._halt_notebook,
                       test=self._conf_test,
                       validate=self._conf_validate,
                       label=self.label
                      )
    
    @property
    def databunch(self):
        try:
            return self._databunch
        except: pass

    @databunch.setter
    def databunch(self, value):
        try:
            self.train_dl = value.train_dl
            self.valid_dl = value.valid_dl
            self.test_dl = value.test_dl
            self._databunch = value
        except:
            raise TypeError('A valid "databunch" must have train_dl and valid_dl properties, like a Databunch')
        
    def _set_post_forward(self, post_forward, model, loss):
        if post_forward:
            self.post_forward = post_forward
            return
        if post_forward == False:
            self.post_forward = identity
        try:
            self.post_forward = model.post_forward
            return
        except:
            self.post_forward = identity
            for l, func in POST_FORWARD.items():
                try:
                    if loss.__class__ == l:
                        if func:
                            self.post_forward = func
                        return
                except: pass
        if not self.silent:
            print('Warning, assuming no post_forward is needed (unknown loss function). Pass post_forward=False to suppress this warning.')
       
    @property
    def evaluator_class(self):
        try:
            return self._evaluator_class
        except:
            if self._torchevaluator:
                return EvaluatorTorch
            else:
                return EvaluatorSK
        
    @property
    def evaluator(self):
        """
        The (PipeTorch) evaluator that is used to record training progress
        """
        try:
            return self._evaluator
        except:
            self._evaluator = self.evaluator_class(self, *self.metrics, label=self.label)
            return self._evaluator
       
    @evaluator.setter
    def evaluator(self, value):
        self._evaluator = value
    
    def __repr__(self):
        return 'Trainer( ' + repr(self.model) + ')'
       
    def cpu(self):
        """
        Configure the trainer to train on cpu
        """
        if self._gpu is not False:
            self._gpu = False
            try:
                del self._device
            except: pass

    @property
    def device(self):
        try:
            return self._device
        except:
            self._device = None
            if self._gpu is False:
                if not self.silent:
                    print('Working on cpu, note that when training a big network you should train on GPU if available.')
                self._device = torch.device('cpu')
            elif type(self._gpu) == int:
                if not self.silent:
                    print(f'Working on cuda:{self._gpu}')
                assert self._gpu < torch.cuda.device_count(), f'You must choose a number of an existing GPU, {self._gpu} is too high. Use !nvidia-smi to inspect which GPU\'s there are and what theri current load is.'
                self._device = torch.device(f'cuda:{self._gpu}')
            elif self._gpu == True:
                device = self._get_first_gpu() or torch.device('cpu')
                if device is not None and device.type == 'cpu':
                    if device != self._device:
                        self._device = device
                    if not self.silent:
                        print('No GPU is available, using CPU instead.')
                elif device != self._device:
                    self._device = device
                    if not self.silent:
                        print(f'Training on {device.type}:{device.index}.')                           
            if self._device is None:
                if not self.silent:
                    print('Working on cpu because an exception occurred. Note that when training a big network you should train on GPU if available.')
                self._device = torch.device('cpu')
            return self._device
        
    def _get_first_gpu(self):
        try:
            import GPUtil
        except:
            assert False, 'You must install GPUtil to use gpu=True'
        d = GPUtil.getAvailable(order = 'memory', limit = 1, maxLoad = 0.7, maxMemory = 0.8, includeNan=False, excludeID=[], excludeUUID=[])
        if len(d) > 0:
            return torch.device(f'cuda:{d[0]}')
    
    #def _get_first_tpu(self):
    #    if os.environ['COLAB_TPU_ADDR']:
    #        try:
    #            import torch_xla.core.xla_model as xm
    #            return xm.xla_device()
    #        except: pass
    
    @device.setter
    def device(self, value):
        self._device = value
  
    @property
    def gpu(self):
        try:
            return self._gpu
        except:
            self._gpu = True
            return self._gpu
        
    @gpu.setter
    def gpu(self, value):
        """
        Configure the trainer to train on gpu, see to(device)
        """
        try:
            if self._gpu == value and value is not True:
                return
        except: pass
        self._gpu = value
        try:
            del self._device
        except: pass
        
    def cleanup(self):
        for t in self.alltrainers:
            t.to(torch.device('cpu'))
        gc.collect()
        torch.cuda.empty_cache()
            
    @property
    def metrics(self):
        """
        Returns: list of metrics that is collected while training
        """
        return self._metrics
    
    @metrics.setter
    def metrics(self, value):
        """
        Sets the metric(s) that are collected while training
        """
        if value is None:
            value = []
        else:
            try:
                iter(value)
            except:
                value = [value]
        try:
            if value == self._metrics:
                return
        except: pass
        self._metrics = value
        if len(value) > 0:
            module = value[0].__module__.split('.')[0]
            self._torchevaluator = (module == 'torcheval')
            if self._torchevaluator:
                for m in value[1:]:
                    assert m.__module__.split('.')[0] == 'torcheval', 'You cannot currently mix torcheval with non-torcheval metrics'
        else:
            self._torchevaluator = True
        
    @property
    def epochidstr(self):
        return f'{self.epochid:>{self._epochspaces}}' if self.cycle >= 1 else f'{self.subepochid:{self._epochspaces+3}.2f}'
        
    @property
    def epochs(self):
        try:
            if self._epochs is None:
                return self.lead_trainer.epochs
        except:
            try:
                assert self._epochs is not None or self.lead_trainer is not None, \
                    "Illegal call on epochs when no training has been prepared"
            except:
                self._epochs = None
                return self.lead_trainer.epochs
        
    @property
    def databunch(self):
        """
        Returns: the databunch that is used
        
        thows an exception if no databunch has been configured
        """
        return self._databunch

    @databunch.setter
    def databunch(self, db):
        """
        Setter to use a databunch. The databunch object must have at least
        a train_dl and a valid_dl property, and optional a test_dl. These
        are often PyTorch DataLoaders, but can be any iterable over a
        DataSet.
        """
        
        assert hasattr(db, 'train_dl'), 'A single data source must be an object with a train_dl property (like a databunch)'
        assert hasattr(db, 'valid_dl'), 'A single data source must be an object with a valid_dl property (like a databunch)'
        self._databunch = db
        self.train_dl = self.databunch.train_dl
        self.valid_dl = self.databunch.valid_dl
        try:
            self.test_dl = self.databunch.test_dl
        except: pass

    @property
    def lr(self):
        """
        return: the learning rate that was set, could be an interval
        """
        return self._lr
        
    @lr.setter
    def lr(self, lr):
        """
        Sets the learning rate that is used for training. You can either use a single value
        for a fixed lr, a tuple with an interval of two values for a linear decaying 
        scheduler, or a tuple with an interval of two values for a OneCyleLR scheduler.
        The allocation of a scheduler can be overruled by setting a scheduler manually.
        
        If the lr did not change, nothing happens, otherwise a new optimizer is created
        when needed.
        """
        if type(lr) is tuple:
            lr = tuple(sorted(lr))
        elif type(lr) is list:
            lr = sorted(lr)
        try:
            if self._lr == lr:
                return
        except: pass
        try:
            if lr == self._lr:
                return
        except: pass
        self.del_optimizer()
        self._lr = lr

    def set_lr(self, lr):
        """
        sets the learning rate without changing the learning rate settings
        the scheduler or optimizer. is used by tuners like find_lr.
        """
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr
            
    @property
    def min_lr(self):
        """
        the learning rate or lowest of an interval of learning rates
        """
        try:
            return self.lr[0]
        except:
            return self.lr

    @property
    def max_lr(self):
        """
        the learning rate or highest of an interval of learning rates
        """
        try:
            return self.lr[1]
        except: pass
        try:
            return self.lr[0]
        except: pass
        return self.lr

    @property
    def weight_decay(self):
        """
        Returns: the current value for the weight decay regularization
        """
        return self._weight_decay

    @weight_decay.setter
    def weight_decay(self, value):
        """
        Sets the weight decay regularization
        only works when the optimizer class supports this.
        """
        try:
            if self._weight_decay == value:
                return
        except: pass
        self.del_optimizer()
        self._weight_decay = value

    @property
    def betas(self):
        """
        Returns the betas parameter for the optimizer
        """
        return self._betas

    @betas.setter
    def betas(self, value):
        """
        Sets the betas parameter that is used to instantiate an optimizer
        only works when the optimizer class supports this.
        """
        try:
            if self._betas == value:
                return
        except: pass
        self.del_optimizer()
        self._betas = value

    @property
    def optimizer(self):
        """
        Returns: an optimizer for training the model, using the applied
        configuration (e.g. weight_decay, betas, learning_rate).
        If no optimizer exists, a new one is created using the configured
        optimizerclass (default: AdamW) and settings.
        """
        try:
            return self._optimizer
        except:
            if type(self._optimizer_class) == str:
                if self._optimizer_class.lower() == 'adam':
                    self._optimizer_class = Adam
                elif self._optimizer_class.lower() == 'adamw':
                    self._optimizer_class = AdamW
                elif self._optimizer_class.lower() == 'rmsprop':
                    self._optimizer_class = RMSprop
                elif self._optimizer_class.lower() == 'adadelta':
                    self._optimizer_class = Adadelta
                elif self._optimizer_class.lower() == 'adagrad':
                    self._optimizer_class = Adagrad
                elif self._optimizer_class.lower() == 'Adamax':
                    self._optimizer_class = Adamax
                elif self._optimizer_class.lower() == 'lbfgs':
                    self._optimizer_class = LBFGS
                elif self._optimizer_class.lower() == 'sgd':
                    self._optimizer_class = SGD
                elif self._optimizer_class.lower() == 'sparseadam':
                    self._optimizer_class = SparseAdam
                else:
                    raise ValueError(f'Unsupported value {self._optimizer_class} given as optimizer.')
            if self.weight_decay is not None:
                if self.betas is not None:
                    f = partial_replace_args(self._optimizer_class, weight_decay=self.weight_decay, betas=self.betas)
                else:
                    f = partial_replace_args(self._optimizer_class, weight_decay=self.weight_decay)
            elif self.betas is not None:
                f = partial_replace_args(self._optimizer_class, betas=self.betas)
            else:
                f = self._optimizer_class
            self._optimizer = f(self.model.parameters(), lr=self.min_lr)
            return self._optimizer

    @optimizer.setter
    def optimizer(self, value):
        """
        Sets the optimizer class to use. 
        """
        try:
            if self._optimizer_class == value:
                return
        except: pass
        self._optimizer_class = value
        self.del_optimizer()
        
    def del_optimizer(self):
        try:
            del self._optimizer
        except: pass
        self.del_scheduler()

    def del_scheduler(self):
        try:
            del self._scheduler
        except: pass

    def scheduler_step(self):
        try:
            self.scheduler.step()
        except ValueError:
            del self._scheduler
            self.scheduler.step()
        
    @property
    def scheduler(self):
        """
        Returns: scheduler that is used to adapt the learning rate

        When you have set a (partial) function to initialize a scheduler, it should accepts
        (optimizer, lr) as its parameters. Otherwise, one of three standard
        schedulers is used based on the value of the learning rate. If the learning rate is 
        - float: no scheduler is used
        - [max, min]: a linear decaying scheduler is used. 
        - (max, min): a OneCyleLR scheduler is used.
        """
        try:
            return self._scheduler
        except:
            #steps = int(round((len(self.train_dl) * self.cycle_epochs)))
            if self._scheduler_class is None:
                try:
                    self.lr[1]
                    if type(self.lr) == tuple:
                        schedulerclass = OneCycleLR
                    elif type(self.lr) == list:
                        schedulerclass = ConstantLR
                    else:
                        raise NotImplementedError(f'Provide either an single value learning rate for a Uniform scheduler, list [low, high] for a Linear Decay, or tuple (low, high) for a OneCycleLR scheduler')
                except:
                    schedulerclass = UniformLR
            else:
                schedulerclass = self._scheduler_class
            if schedulerclass == ConstantLR:
                min_lr = self.min_lr
                max_lr = self.max_lr
                try:
                    min_lr = min_lr[0]  # working with parameter groups
                except: pass
                try:
                    max_lr = max_lr[0]  # working with parameter groups
                except: pass
                factor = (min_lr / max_lr) ** (1 / self._scheduler_epochs)
                self._scheduler = ConstantLR(self.optimizer, factor,
                                  self._scheduler_epochs)
            elif schedulerclass == OneCycleLR:
                total_steps = math.ceil(len(self.train_dl) * self.cycle)
                if total_steps > 1:
                    self._scheduler = OneCycleLR(self.optimizer, 
                                      self.max_lr, total_steps=total_steps)
                else:
                    self._scheduler = UniformLR(self.optimizer, self.max_lr)
            else:
                try:
                    self._scheduler = schedulerclass(self.optimizer, 
                                  self.lr)
                except:
                    raise NotImplementedError(f'The provided {schedulerclass} function does not work with ({self.optimizer}, {self.lr}, {self._scheduler_epochs}, {len(self.train_dl)}) to instantiate a scheduler')
            return self._scheduler
    
    @scheduler.setter
    def scheduler(self, value):
        """
        Sets the schedulerclass to use. 
        
        At this moment, there is no uniform way to initialize all PyTorch schedulers. 
        PipeTorch provides easy support for using a scheduler through the learning rate:
        - float: no scheduler is used
        - [max, min]: a linear annealing scheduler is used. 
        - (max, min): a OneCyleLR scheduler is used.
        
        To use an other scheduler, set this to a (partial) function that accepts
        the following parameters: (optimizer instance, learning rate)
        """
        try:
            del self._scheduler
        except: pass
        self._scheduler_class = value
    
    @property
    def valid_ds(self):
        return self.valid_dl.dataset

    @property
    def train_ds(self):
        return self.train_dl.dataset

    @property
    def test_ds(self):
        return self.test_dl.dataset

    @property
    def train_Xy_cpu(self):
        for batch in self.train_dl:
            yield batch
    
    @property
    def valid_Xy_cpu(self):
        for batch in self.valid_dl:
            yield batch
    
    @property
    def test_Xy_cpu(self):
        for batch in self.test_dl:
            yield batch
    
    @property
    def train_Xy(self):
        for batch in self.train_dl:
            yield self._batch_to(batch)
    
    @property
    def valid_Xy(self):
        for batch in self.valid_dl:
            yield self._batch_to(batch)
    
    @property
    def test_Xy(self):
        for batch in self.test_dl:
            yield self._batch_to(batch)
    
    def _batch_to(self, batch):
        *X, y = batch
        X = ( x.to(self.model.device, non_blocking=True) for x in X )
        y = y.to(self.model.device, non_blocking=True)
        return *X, y
    
    @property
    def valid_tensors(self):
        return self.valid_dl.dataset.tensors

    @property
    def train_tensors(self):
        return self.train_dl.dataset.tensors

    @property
    def test_tensors(self):
        return self.test_dl.dataset.tensors

    @property
    def train_X(self):
        return self.train_tensors[0]

    @property
    def train_y(self):
        return self.train_tensors[-1]

    @property
    def valid_X(self):
        return self.valid_tensors[0]

    @property
    def valid_y(self):
        return self.valid_tensors[-1]

    @property
    def test_X(self):
        return self.test_tensors[0]

    @property
    def test_y(self):
        return self.test_tensors[-1]
    
    @property
    def model(self):
        """
        When a device is configured to train the model on, the model
        is automatically transferred to the device. A device property
        is set on the model to transfer the data to the same device
        as the model before using.
        
        Returns: the model 
        """
        try:
            if self.device is not self._model.device:
                self._model.to(self.device, non_blocking=True)
                self._model.device = self.device
                try:
                    del self._optimizer
                except: pass
                if self.device.type == 'cpu':
                    gc.collect()
                    torch.cuda.empty_cache()
        except:
            try:
                self._model.to(self.device, non_blocking=True)
                self._model.device = self.device
                #print('change device')
                try:
                    del self._optimizer
                except: pass
            except: pass
        return self._model

    def to(self, device):
        self._model.device = device
        self._model.to(device, non_blocking=True)
        self.evaluator.reset()
        self.del_optimizer()
    
    @property
    def model_size(self):
        """
        Returns the expected model size in bytes. The actual amount of memory occupied will be much greater,
        since an optimizer in general will triple the size used and there is also memory needed to compute the
        graph and for CUDA overhead.
        """
        try:
            return self._model_size
        except:
            self._model_size = 0
            for param in self.model.parameters():
                self._model_size += param.nelement() * param.element_size()
            return self._model_size
        
    @property
    def cycle(self):
        if self._cycle is None:
            if self.lead_trainer is not None:
                return self.lead_trainer.cycle
            else:
                return 1
        return self._cycle
    
    @cycle.setter
    def cycle(self, value):
        self._cycle = value
    
    @property
    def epochs(self):
        if self._epochs is None:
            if self.lead_trainer is not None:
                return self.lead_trainer.epochs
            else:
                raise ValueError("Epochs must be set")
        return self._epochs
    
    @epochs.setter
    def epochs(self, value):
        self._epochs = value
    
    @property
    def cotrainers(self):
        try:
            return self._cotrainers
        except:
            self._cotrainers = []
            return self._cotrainers
    
    @property
    def multiple_trainers(self):
        return len(self.cotrainers) > 0 or type(self) == CoTrainer
    
    @property
    def alltrainers(self):
        try:
            return self._alltrainers
        except:
            self._alltrainers = [self] + self.cotrainers
            return self._alltrainers
    
    def register_cotrainer(self, cotrainer):
        assert type(cotrainer) == CoTrainer and cotrainer.lead==self, \
            'Can only assign cotrainers of the CoTrainer class that use this trainer as lead'
        self.cotrainers.append(cotrainer)
        try:
            del self._alltrainers
        except: pass
    
    @model.setter
    def model(self, value):
        self._model = value
        self.del_optimizer()
        try:
            del self._model_size
        except: pass
    
    def parameters(self):
        """
        Prints the (trainable) model parameters
        """
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                print(name, param.data)

    def reset_model(self):
        """
        Resets all weights in the current model
        
        refs:
            - https://discuss.pytorch.org/t/how-to-re-set-alll-parameters-in-a-network/20819/6
            - https://stackoverflow.com/questions/63627997/reset-parameters-of-a-neural-network-in-pytorch
            - https://pytorch.org/docs/stable/generated/torch.nn.Module.html
        """

        @torch.no_grad()
        def weight_reset(m: nn.Module):
            # - check if the current module has reset_parameters & if it's callabed called it on m
            reset_parameters = getattr(m, "reset_parameters", None)
            if callable(reset_parameters):
                m.reset_parameters()

        # Applies fn recursively to every submodule see: https://pytorch.org/docs/stable/generated/torch.nn.Module.html
        self.model.apply(fn=weight_reset)
        self.epochid = 0
        try:
            del self._optimizer
        except: pass       
                
    def forward(self, *X):
        """
        Returns the results of the model's forward on the given input X.
             
        Arguments:
            *X: tensor or collection of tensors
                the tensor of collection of tensors that is passed to
                the forward of the model. The inputs are automatically 
                transfered to the same device as the model is on.
        
        Returns: tensor
            outputs that are returned by first the forward pass on
            the model.
        """
        #X = [ x.to(self.model.device, non_blocking=True) for x in X ]
        if self._debug:
            self.lastx = X
            self.lastyfw = self.model(*X)
            return self.lastyfw
        return self.model(*X)
       
    def predict(self, *X):
        """
        Returns model predictions for the given input.
        The difference with forward is that the outputs of the model
        are optionally processed by a post_forward (for classification).
        
        Arguments:
            *X: tensor or collection of tensors
                the tensor of collection of tensors that is passed to
                the forward of the model. The inputs are automatically 
                transfered to the same device as the model is on.
        
        Returns: tensor
            Predictions that are returned by first the forward pass on
            the model and optionally a post_forward for classification
            tasks
        """
        self.post_forward(self.forward(*X))

    def post_forward(self, y):
        """
        For classification tasks, training may require a different 
        pred_y than the evaluation metrics do. Typically, the predictions
        are logits or an estimated likelihood (e.g. 0.2), while the 
        evaluation function need a class label (e.g. 0 or 1). Using
        PipeTorch, you need to add a post_forward(y) method to your model,
        that will be called on the predictions before they are passed
        to the evaluation functions. 
        
        Returns: tensor
            If the model has a post_forward to convert pred_y to predictions,
            this returns the the results calling post_forward, otherise,
            it will just return pred_y
        """
        raise ValueError('The Trainer was somehow not initialized with a post_forward')

    @property
    def subepochid(self):
        r = (self.epochid + self.batch / len(self.train_dl))
        return round(r / self.cycle) * self.cycle
    
    def list_commits(self):
        """
        Returns: a list of the keys of committed (saved) models, during 
        or after training.
        """
        return self._commit.keys()

    def list_models(self, folder=None, hash=True, modelname=True, filename=None, extension=None):
        """
        Returns a list of the path of (possibly) compatible stored files.
        
        Normally the hash_code of the model is used to scan for 
        possible matches, but in case there are multiple matches
        and additional modelname can be used or the filename can be specified.
        
        Args:
          folder: str (None)
            the folder to search for files, or None for the current folder
          filename: str (None)
            this overrules everything and just uses this exact filename
          hash: bool (True)
            a hashcode is used based on the model parameter sizes to match
            only files with compatible parameter shapes. If only one such 
            file is found, the use of filename is ignored.
          modelname: str/path (None)
            The modelname should match the start of the filename. If None, the 
            current notebook name is used. This can help to additionally filter
            if there are several saved files that match the model hash (because
            several notebooks use a model with the same parameters).
          extension: str (None)
            when None, an extension .pyt_version is used. Alternatively,
            the extension can be given
        """
        extension = extension or 'torch'
        folder = folder or '.'
        if filename is not None:
            flist = [ p for p in Path(folder).glob(f'{filename}') if p.is_file() ]
            if len(flist) == 0:
                flist = [ p for p in Path(folder).glob(f'{filename}.{extension}') if p.is_file() ]
            return flist
        if modelname is True:
            modelname = self.label
        else:
            modelname = modelname or ''
        if hash is True:
            hash = self._model_hash()
        flist = [ p for p in Path(folder).glob(f'{modelname}*.{extension}') if p.is_file() ]
        if hash is not None:
            hlist = [ p for p in Path(folder).glob(f'*_{hash}*.{extension}') if p.is_file() ]
            inter = set(flist).intersection(set(hlist))
            if len(inter) == 1:
                return list(inter)
            elif len(hlist) == 1:
                return hlist
        return flist

    def purge_models(self, folder=None, hash=True, modelname=True, filename=None):
        for f in self.list_models(folder, hash, modelname, filename):
            Path(f).unlink()
    
    def purge_train(self, folder=None, hash=True, modelname=True, filename=None):
        for f in self.list_models(folder, hash, modelname, filename, extension='train'):
            Path(f).unlink()
    
    def list_train(self, folder=None, hash=True, modelname=True, filename=None, extension='train'):
        r = []
        for f in self.list_models(folder, hash, modelname, filename, extension):
            data = torch.load(ftr)
            r.append((f.parts[-1], data['label'], data['metrics'], data['epoch'], 
                     data['model_params'], data['validloss'], data['validmetric'],
                     data['lr'], data['weight_decay'], data['torch_version'],
                     data['optimizer'] is not None))
        return pd.DataFrame(r, columns=['filename', 'label', 'metrics', 'epoch', 'params',
                                       'valid_loss', 'valid_metric', 'lr',
                                       'weight_decay', 'torch_version', 'has_opt'])

    def commit(self, label):
        """
        Save the model and optimizer state, allowing to revert to a 
        previous state/version of the model.
        
        Arguments:
            label: str
                The key to save the model under
        """        
        self._commit[label] = self.state_dict()
        
    def _model_hash(self):
        return hashlib.blake2b(self._model_params().tobytes(), digest_size=20).hexdigest()
        
    def _model_params(self):
        return np.concatenate([ torch.tensor(p.shape).numpy() 
                              for p in self.model.parameters()])
            
    def _model_filename(self, folder=None, hash=True, modelname=True, filename=None, extension=None, epoch=False):
        if folder is None:
            folder = '.'
        if filename is not None:
            return f'{folder}/{filename}'
        path = f'{folder}/'
        if modelname is True:
            path += self.label
        elif type(modelname) == str:
            path += modelname
        if hash:
            path = f'{path}_{self._model_hash()}'
        if epoch:
            if self.batch == 0:
                path = f'{path}_epoch{self.epochid}'
            else:
                path = f'{path}_epoch{self.subepochid:0.2f}'
        return f'{path}.{extension or "torch"}'
        
    def save(self, folder=None, hash=True, modelname=True, filename=None, extension='torch', epoch=False):
        """
        Saves a (trained) model to file. This will only save the model parameters. To load the model, you will
        first have to initialize a model with the same configuration, and then use `Trainer.load(path)` to load
        the model from file.
        
        Aruments:
            folder: str (None)
                folder to save the model, default is the current folder
            filename: str (None)
                the basename of the saved file, default is the classname
            extension: str (None)
                the extension of the saved file, default is pyt with the pytorch version name
        """
        path = self._model_filename(folder, hash, modelname, filename, extension, epoch)
        torch.save(self.model.state_dict(), path)
        print(f'Saved the model as {path}')
        
    def save_trainer(self, folder=None, hash=True, modelname=True, filename=None, extension='train', epoch=True, optim=False):
        """
        Saves the trainer state to file, including model parameters, optimizer, current
        epoch and training history. 
        
        The saved state can be loaded to continue training from the same point. 
        For this, a trainer must be instantiated with an instance of the same class,
        instantiated dataloaders, the same loss function, metrics, etc. Because these
        cannot be inferred from the data.
        
        Arguments:
            folder: str (None)
                folder to save the model, default is the current folder
            filename: str (None)
                the basename of the saved file, default is the classname
            extension: str ('train')
                the extension of the saved file
            optim: bool (False)
                If True, the optimizer state is also saved, this roughly triples 
                the size of the saved file, but allows to resume training
                from the exact same state.
        """
        path = self._model_filename(folder, hash, modelname, filename, extension=extension, epoch=epoch)
        torch.save(self.state_dict(optim=optim), path)
        if not self.silent:
            print(f'Saved the model as {path}')
        
    def state_dict(self, optim=False):
        """
        Returns a dictionary with the current trainer state. 
        
        The state includes
        information that may help to recognize a saved train state, such as
        the pytorch version, shapes over the model parameters, epoch, label, 
        metrics, last validloss and validmeric.
        
        Args:
            optim: bool (False)
                if True, the optimizer state is included. This often triples the size
                of the saved state but can allows to resume training in the exact same
                state.
        """
        metrics = [ f.__name__ for f in self.evaluator.metrics ]
        try:
            results = self.evaluator.results
            results = results[results.model == self.label]
            validloss = results.value[results.metric == 'loss'].iloc[-1]
            if len(metrics) > 0 and results is not None:
                validmetric = results.value[results.metric == metrics[0]].iloc[-1]
            else:
                validmetric = None
            results = results.to_csv()
        except:
            results = None
            validmetric = None
            validloss = None

        model = { k: v.cpu() for k, v in self.model.state_dict().items() }
        opt = self.optimizer.state_dict() if optim else None
        return {'model_params': self._model_params(),
                'model': model,
                'torch_version': torch.__version__,
                'optimizer': opt, 
                'epoch': self.epochid, 
                'optimizer_class' : self._optimizer_class,
                'results': results,
                'betas': self.betas, 
                'weight_decay': self.weight_decay, 
                'lr': self.lr,
                'label': self.label, 
                'metrics': metrics,
                'validloss': validloss,
                'validmetric': validmetric}
        
    def load(self, folder=None, hash=True, modelname=True, filename=None, extension='torch'):
        """
        Load a saved (trained) model from file. For this to work, the model for this trainer has to be configured
        in the exact same way as the model that was saved. This will only load the model parameters.
        
        Aruments:
            folder: str (None)
                folder to save the model, default is the current folder
            filename: str (None)
                the basename of the saved file, default is the classname
            extension: str (None)
                the extension of the saved file, default is pyt with the pytorch version name
        """
        if modelname is True:
            modelname = self.label
        files = self.list_models(folder=folder, hash=hash, modelname=modelname, filename=filename, extension=extension)
        assert len(files) > 0, 'No matching file found'
        assert len(files) < 2, f'Multiple matching files found, use filename= to distinguish between {files}'
        data = torch.load(files[0])
        try:
            self.model.load_state_dict(data)
        except:
            raise ValueError('Failed to load the data in the model, perhaps the model has changed?')
        
    def load_trainer(self, folder=None, hash=True, modelname=True, filename=None, extension='train'):
        """
        Load a saved trainer state from file. 
        
        Typically a .train file that was saved using Trainer.save. 
        
        This trainer has te be initialized with a model with matching
        parameters. To continue training you wil
        trainer is initialized with the same model class and optimizer class 
        (the parameters must match). The continue training from the same point, the
        trainer must also be seeded with dataloaders and configured with the same
        metrics.
        
        Aruments:
            folder: str (None)
                folder to save the model, default is the current folder
            filename: str (None)
                the basename of the saved file, default is the classname
            extension: str ('.train')
                the extension of the saved file, default is pyt with the pytorch version name
        """
        if modelname is True:
            modelname = self.label
        files = self.list_models(folder=folder, hash=hash, modelname=modelname, filename=filename, extension=extension)
        assert len(files) > 0, 'No matching file found'
        assert len(files) < 2, 'Multiple matching files found, use filename='
        data = torch.load(files[0])
        self.load_state_dict(data)
        
    def load_state_dict(self, state):
        metrics = []
        for f in state['metrics']:
            try:
                metrics.append(eval(f))
            except:
                raise ValueError(f"Cannot load training session because the metric {f} is not defined")
        assert (state['model_params'] == self._model_params()).all(), \
            'The parameters shapes of the model do not match the parameter shapes of the stored file'
        self.model.load_state_dict(state['model'])
        self.epochid = int(math.ceil(state['epoch']))
        self.betas = state['betas']
        self.weight_decay = state['weight_decay']
        self.lr = state['lr']
        self.optimizer=state['optimizer_class']
        if state['optimizer'] is not None:
            self.optimizer.load_state_dict(state['optimizer'])
        if type(self) is not CoTrainer:
            self.metrics = metrics
        if state['results']:
            results = pd.read_csv(StringIO(state['results']))
            self.evaluator.appendresults(results)
        self.label = state['label']
        
    def to_trt(self):
        """
        Converts the (trained) model into a TRT model that can be used on a Jetson
        
        Returns: TRTModule
            The converted model
        """
        from torch2trt import torch2trt
        x = next(iter(self.train_Xy))[1]
        return torch2trt(self.model, [x])
        
    def save_trt(self, folder=None, hash=True, modelname=True, filename=None, extension='trt'):
        """
        Converts the (trained) model to TRT and saves it.
        
        Aruments:
            folder: str (None)
                folder to save the model, default is the current folder
            filename: str (None)
                the basename of the saved file, default is the classname
            extension: str ('trt')
                the extension of the saved file
        """
        path = self._model_filename(folder, filename, extension)
        torch.save(self.to_trt().state_dict(), path)
        if not self.silent:
            print(f'Saved the TRT model as {path}')
        
    def save_onnx(self, folder=None, hash=True, modelname=True, filename=None, extension='onnx'):
        """
        Converts the (trained) model to ONNX and saves it.
        
        Aruments:
            folder: str (None)
                folder to save the model, default is the current folder
            filename: str (None)
                the basename of the saved file, default is the classname
            extension: str ('onnx')
                the extension of the saved file
        """
        path = self._model_filename(folder, filename, extension)
        x = next(iter(self.train_Xy))[1][:1]
        torch.onnx.export(self.model, x, path, verbose=True)
        if not self.silent:
            print(f'Savfed the ONNX model as {path}')
        
        
    def revert(self, label):
        """
        Revert the model and optimizer to a previously commited state, 
        and deletes the commit point to free memory. Prints a warning
        when the label was not found.
        
        Arguments:
            label: str
                The key under which the model was commited
        """
        if label in self._commit:
            self.load_state_dict(self._commit.pop(label))
        else:
            print('commit point {label} not found')
    
    def checkout(self, label):
        """
        Loads a previously commited state of the model and optimizer 
        but keeps the commit point. Prints a warning
        when the label was not found.
        
        Arguments:
            label: str
                The key under which the model was commited
        """
        if label in self._commit:
            self.load_state_dict(self._commit[label])
        else:
            print('commit point {label} not found')

    def reset(self):
        """
        Resets the cached results, for tuning purposes.
        """
        self.reset_model()
            
    def remove_checkpoint(self, label):
        """
        Removes a previously committed state of the model.
        
        Arguments:
            label: str
                The key under which the model was commited
        """
        self._commit.pop(label)

    def purge(self, label):
        """
        Switches the model and optimizer to a previously commited state, 
        and keeps only that commit point and removes all other versions.
        
        Arguments:
            label: str
                The key under which the model was commited
        """
        if label in self._commit:
            self.checkout(label)
            self._commit = { l:s for l,s in self._commit.items() if l == label }
        else:
            print(f'commit point {label} not found')

    def _loss_xy(self, *X, y=None):
        """
        Computes predictions for the given X.
        
        Arguments:
            *X: tensor
                inputs that are used by the forward of the model
            y: tensor
                ground truth labels, the predictions are compared against
        
        Returns: (float, tensor)
            a tuple with the loss for the predictions on X,
            and a tensor with the predicted values
        """
        assert y is not None, 'Call _loss_xy with y=None'
        if self._debug:
            self.lasty = y
        y_pred = self.forward(*X)
        if self._debug:
            self.lastyfw = y_pred
        loss = self.loss(y_pred, y)
        return loss, y_pred 
    
    def _loss_forward_xy(self, *X, y=None):
        """
        Computes predictions for the given X.
        
        Arguments:
            *X: tensor
                inputs that are used by the forward of the model
            y: tensor
                ground truth labels, the predictions are compared against
        
        Returns: (float, tensor)
            a tuple with the loss for the predictions on X,
            and a tensor with the predicted values
        """
        loss, y_pred = self._loss_xy(*X, y=y)
        y_pred = self.post_forward(y_pred)
        if self._debug:
            self.lastypfw
        return loss, y_pred 
    
    def loss_dl(self, dl):
        """
        Iterates over the given dataloader, the loss is computed in
        evaluation mode and accumulated over the dataset.
        
        Arguments:
            dl: DataLoader
                the dataloader that is used to iterate over.
        
        Returns: float 
            weighted average loss over the given dataloader/set.
        """
        if not dl:
            dl = self.valid_Xy_cpu
        meanloss = Mean(device=self.device)
        leny = 0
        with self.eval_mode:
            for batch in dl:
                leny = len(batch[0])
                batch = self._batch_to(batch)
                *X, y = batch
                if self._debug:
                    self.lasty = y
                y_pred = self.forward(*X)
                l = self.loss(y_pred, y)
                meanloss.update(l, weight=leny)
        return meanloss.compute()

    def validate_loss(self):
        """
        Returns: weighted average loss over the validation set, or
        the data that is provided.
        
        """
        return self.loss_dl(self.valid_Xy_cpu)

    @property
    def eval_mode(self):
        """
        A ContextManager to put the model in evaluation mode
        """
        class CM(object):
            def __init__(self, trainer):
                self.trainer = trainer
            def __enter__(self):
                self.trainer.model.eval()
                self.prev = torch.is_grad_enabled()
                torch.set_grad_enabled(False)
                return self.trainer.model
            def __exit__(self, type, value, traceback):
                torch.set_grad_enabled(self.prev)
                if self.prev:
                    self.trainer.model.train()
                else:
                    self.trainer.model.eval()
        return CM(self)

    @property
    def co_eval_mode(self):
        """
        A ContextManager to put the model in evaluation mode
        """
        class CM(object):
            def __init__(self, trainer):
                self.trainer = trainer
            def __enter__(self):
                for t in self.trainer.alltrainers:
                    t.model.eval()
                self.prev = torch.is_grad_enabled()
                torch.set_grad_enabled(False)
                return self.trainer.model
            def __exit__(self, type, value, traceback):
                torch.set_grad_enabled(self.prev)
        return CM(self)

    @property
    def train_mode(self):
        """
        A ContextManager to put the model in training mode
        """
        class CM(object):
            def __init__(self, trainer):
                self.trainer = trainer
            def __enter__(self):
                self.trainer.model.train()
                self.prev = torch.is_grad_enabled()
                torch.set_grad_enabled(True)
                return self.trainer.model
            def __exit__(self, type, value, traceback):
                torch.set_grad_enabled(self.prev)
                self.trainer.model.eval()
        return CM(self)

    @property
    def co_train_mode(self):
        """
        A ContextManager to put the model in training mode
        """
        class CM(object):
            def __init__(self, trainer):
                self.trainer = trainer
            def __enter__(self):
                for t in self.trainer.alltrainers:
                    t.model.train()
                self.prev = torch.is_grad_enabled()
                torch.set_grad_enabled(True)
                return self.trainer.model
            def __exit__(self, type, value, traceback):
                torch.set_grad_enabled(self.prev)
        return CM(self)
    
    def _cycle_init(self):
        self.evaluator.reset_metrics()
    
    def _test_finish(self):
        self._last_test_metrics = self.evaluator.compute_test_metrics()
        self._store_metrics(self._last_test_metrics, 'test')
        return self._last_test_metrics
    
    def _validate_finish(self):
        self._last_valid_metrics = self.evaluator.compute_valid_metrics()
        self._store_metrics(self._last_valid_metrics, 'valid')
        return self._last_valid_metrics
    
    def _train_finish(self):
        self._last_train_metrics = self.evaluator.compute_train_metrics()
        self._store_metrics(self._last_train_metrics, 'train')
        return self._last_train_metrics
    
    def _validate_accumulate(self, *X, y, pbar):
        loss, y_pred = self._loss_forward_xy(*X, y=y)
        self.evaluator.accumulate_valid_metrics(y, y_pred, loss)
        if pbar is not False:
            if pbar is not None:
                pbar.update(self.valid_dl.batch_size)
        
    def _test_accumulate(self, *X, y, pbar):
        loss, y_pred = self._loss_forward_xy(*X, y=y)
        self.evaluator.accumulate_test_metrics(y, y_pred, loss)
        if pbar is not False:
            if pbar is not None:
                pbar.update(self.test_dl.batch_size)
        
    def _validate(self, pbar=None):
        """
        Run the validation set (in evaluation mode) and store the loss and metrics into the evaluator.
        
        Arguments:
            pbar: tqdm progress bar (None)
                if not None, progress is reported on the progress bar
                
        Returns: float
            weighted average loss over the validation set
        """

        with self.eval_mode:
            for *X, y in self.valid_Xy:
                self._validate_accumulate(*X, y=y, pbar=pbar)
    
    def _store_metrics(self, accumulated_metrics, phase):
        """
        store the validation metrics
        
        returns: dict
            evaluation metrics
        """
        metrics = self.evaluator._store_accumulated_metrics(accumulated_metrics, 
                                                annot={'phase':phase, 'epoch':self.subepochid}, **self._validate_annotation)

    def test(self):
        self._test()
        return self._test_finish()
        
    def _test(self, pbar=None):
        """
        Run the test set (in evaluation mode) and store the loss and metrics into the evaluator.
        Is a helper function of train().
        
        Arguments:
            pbar: tqdm progress bar (None)
                if not None, progress is reported on the progress bar
                
        Returns: float
            weighted average loss over the validation set
        """
        with self.eval_mode:
            for *X, y in self.test_Xy:
                self._test_accumulate(*X, y=y, pbar=pbar)
        
    def _train_batch(self, *X, y=None):
        """
        Train the model on a single batch X, y. The model should already
        be in training mode.
        
        Arguments:
            *X: tensor
                inputs that are used by the forward of the model
            y: tensor
                ground truth labels, the predictions are compared against
        
        Returns: (float, tensor)
            a tuple with the loss for the predictions on X,
            and a tensor with the predicted values
        """
        self.optimizer.zero_grad()
        loss, y_pred = self._loss_xy(*X, y=y)
        loss.backward()
        self.optimizer.step()
        #if self.device and self.device.type == 'xla':
        #    xm.mark_step()
        return loss, y_pred
        
    def _time(self):
        try:
            t = self._start_time
        except:
            t = timeit.default_timer()
        self._start_time = timeit.default_timer()
        return timeit.default_timer() - t
    
    def _cross_validate(self, epochs, lr, cycle=1, silent=True, test=True, earlystop=False, annotation={}, debug=False, repeat=1, separate=False, **kwargs):
        """
        broken
        
        Only works with a Databunch from a DFrame that is configured for n-fold cross validation. 
        The model is trained n times (reinitializing every time), and the average metric is reported 
        over the trials.
        
        Arguments:
            epochs: int
                the maximum number of epochs to train. Training may be terminated early when
                convergence requirements are met.
            lr: float, (float, float) or [float, float]
                the learning rate to use for the optimizer. See lr for train().
            cycle: int (1)
                the number of epochs in a cycle. At the end of each cycle the validation is run.
            earlystop: int (False)
                terminates training when the validation loss has not improved for the last
                earlystop cycles.
            test: bool (False)
                run the test set every cycle (used for n-fold cross validation)
            annotation: {}
                see train(annotation), the cross validator extends the annotation with a folds column.
            **kwargs: passed to train()
        """
        from ..data import Databunch
        test_dl = self.test_dl if test else None
        ys = [None] * self.databunch.folds
        ypreds = [None] * self.databunch.folds
        n = [ 0 ] * self.databunch.folds
        losses = [ np.Inf ] * self.databunch.folds
        tq = tqdm(total=self.databunch.folds * repeat)
        for j in range(repeat):
            for i, data in enumerate(self.databunch.iter_folds()):
                self.reset_model()
                self.train_dl = data.train_dl
                self.valid_dl = data.valid_dl
                self.test_dl = data.test_dl
                self.databunch = data
                self.train(epochs, lr, cycle=cycle, pbar=False, annotation=annotation, 
                              test=test, silent=silent, earlystop=earlystop, 
                              validate=False, **kwargs)
                if self.lowest_validtest_loss < losses[i]:
                    ys[i] = self.lowest_validtest_y
                    ypreds[i] = self.lowest_validtest_y_pred
                    losses[i] = self.lowest_validtest_loss
                    n[i] = len(self.lowest_validtest_y)
                tq.update(1)
        self.train_dl = self.databunch.train_dl
        self.valid_dl = self.databunch.valid_dl
        self.test_dl = self.databunch.test_dl
        tq.close()
        if separate:
            for y, y_pred, eloss, en in zip(ys, ypreds, losses, n):
                metrics = self.compute_metrics(y, y_pred)
                metrics['loss'] = eloss / en
                try:
                    r = pd.concat([r, pd.DataFrame([metrics])])
                except:
                    r = pd.DataFrame([metrics])
        else:  
            y = np.concatenate(ys, axis=0)
            y_pred = np.concatenate(ypreds, axis=0)
            metrics = self.compute_metrics(y, y_pred)
            metrics['loss'] = sum(losses) / sum(n)
            r = pd.DataFrame([metrics])
        return r   
    
    def train(self, epochs, lr=None, cycle=1, halt_notebook=None, 
              optimizer=None, scheduler=False, 
              weight_decay=None, betas=None, 
              save_lowest=False, silent=False, pbar=None,
              targetloss=None, targettrainloss=None, earlystop=False, 
              validate=True, annotation={}, test=False, gpu=None, cleanup=True):
        """
        Train the model for the given number of epochs. Loss and metrics
        are recorded during training in an evaluator. If a model was already
        (partially) trained, training will continue where it was left off.
        
        When called with only epochs and optionally cycle, train() will train multiple models in one
        go if there are cotrainers registered to this Trainer. Any other parameter will have to 
        be set by assigning them to their properties before calling train().
        
        Args:
            epochs: int
                the number of epochs to train the model
            
            lr: float, tuple of floats, or list of floats
                float: set the learning
                (upper, lower): switch the scheduler to OneCycleLR and
                    use a cyclic annealing learning rate
                    between an upper and lower bound.
                [upper, lower]: switch the scheduler to Linear Decay and
                    ufse a linearly decaying learning rate
                    between an upper and lower bound. 
            
            cycle: int or float (1)
                Configures after how many epochs there are in a cycle. 
                the loss and metrics are recorded and reported at the end of every cycle.
                For training on very large training sets, if cycle is set to a whole integer
                faction (e.g. cycle=1/10), then validation is done during after that part of
                every epoch. 
                The cycle setting is remembered for consecutive calls to train.
            
            silent: bool (None)
                whether to report progress. Note that even when silent=True
                the metrics are still logged at the end of every cycle.
                        
            optimizer: PyTorch Optimizer or str (None)
                Changes the configured optimizer to a PyTorch or custom 
                optimizer CLASS (not an instance!) that is used during training.

                You can either provide:
                - an optimizer CLASS from the torch.optim module,
                - a custom optimizer CLASS that obeys the same API, 
                - a partial of an optimizer CLASS with optimization arguments set
                - 'AdamW', 'Adam', 'RMSprop', 'Adadelta', 'Adagrad', 'Adamax', 
                  'LBFGS', 'SGD', or 'SparseAdam'

            scheduler: None, custom scheduler class
                used to adapt the learning rate. Set OneCycleLR or Linear Decay
                through the learning rate. Otherwise, provide a custom
                class/function to initialize a scheduler by accepting
                (optimizer, learning_rate, scheduler_cycle)

            weight_decay: float (None)
                The weight_decay setting for the optimizer. When set on an
                optimizer that does not support this, this will fail.

            betas: float (None)
                The betas setting for the optimizer (mostly momentum). When set 
                on an optimizer that does not support this, this will fail.

            targetloss: float (None)
                terminates training when the validation loss drops below the targetloss.
                
            targettrainloss: float (None)
                terminates training when the train loss drops below the 
                targettrainloss.
                
            earlystop: int (False)
                terminates training when the validation loss has not improved for the last
                earlystop cycles. The model will be reverted to the version at the lowest
                validation loss.
                                
            save_lowest: bool (False)
                when the validation loss is lower than seen before, the model is 
                saved/committed as 'lowest' and can be checked out by calling 
                lowest() on the trainer.
                
            annotation: {}
                At the end of every cycle, the loss and metrics over the train, valid
                and optionally test sets are computed and recorded in a result set. The
                values passed in annotation are stored along with this metrics. Typically, this
                is used with a single trainer that is reused for several 'trials' 
                to analyze how the results changes. Several functions on the resultset
                allow to 'select' results based on these settings, are generate plots
                with these settings as 'series'.
                
            test: bool (False)
                run the test set every cycle (used for n-fold cross validation)
                
            gpu: int/bool (None)
                when set, reassign training to a GPU/CPU. When set to True, the
                GPU with the lowest workload is selected. This does take more time
                to assess the GPU workloads and move the model, but may save time
                when a better option is found.
                See trainer.gpu() for more info.
                
            halt_notebook: bool (None)
                When set, at the end of the session Trainer.save_trainer() and Trainer.halt_notebook() 
                will be executed to save the trainer session (including the model) and terminate 
                the notebook to free resources. 
                By default (None), the settings for initializing the trainer is used (default:True
                because users tend to forget closing their notebooks). Set to False to supress.
                
            cleanup: bool (True)
                When True and halt_notebook=False, at the end of the session, the optimizer is removed
                (freeing op 2/3 memory) and the model is transfered to CPU To release GPU memory.
                
        """
        self._prepare_trainer(lr=lr, epochs=epochs, cycle=cycle, 
              optimizer=optimizer, scheduler=scheduler, 
              weight_decay=weight_decay, betas=betas, 
              save_lowest=save_lowest, silent=silent, 
              pbar=pbar, targetloss=targetloss, targettrainloss=targettrainloss, 
              earlystop=earlystop, validate=validate, annotation=annotation, test=test, gpu=gpu )
        if halt_notebook is None:
            halt_notebook = self._halt_notebook
        cleanup = cleanup and not halt_notebook
        with trainsession(self, silence=self.silent, cleanup=cleanup):
            if lr is None and self.multiple_trainers and not type(self)==CoTrainer:
                self._cotrain(epochs, cycle=cycle)
            else:
                self._cycle_init()
                for i in range(self.epochs):
                    with self.train_mode:
                        for self.batch, (*X, y) in enumerate(self.train_Xy):
                            self._train_one_batch(*X, y=y, record=self.record_this_epoch)
                            self.batch = (self.batch + 1) % len(self.train_dl)
                            if self._check_end_of_cycle(self.batch):
                                self._validate(pbar=self.currentpbar)
                                if self._conf_test:
                                    self._test(pbar=self.currentpbar)
                                self._train_finish()
                                self._validate_finish()
                                if self._conf_test:
                                    self._test_finish()
                                self._report_cycle()
                                #self._cycle_init()
                                self._check_save()
                                if self._check_early_termination():
                                    break
                    if self.terminated:
                        break
            if self._session_closepbar is True:
                try:
                    self.currentpbar.close()    
                except: pass
            if halt_notebook:
                print('Saving the/all trainer sessions to disk and halting the notebook to free up resources')
                print('You can resume this session by instantiating a model and trainer, and calling trainer.load_trainer()')
                print('To prevent autmatic halting the notebook after train(), set halt_notebook=False and please')
                print('remember to shutdown your notebook properly by calling halt_notebook() or using Close and Halt from the menu.')

                for t in self.alltrainers:
                    t.save_trainer()
                self.halt_notebook()
    
    @staticmethod
    def halt_notebook():
        halt_notebook()
    
    def _cotrain(self, epochs, cycle=None):
        self.bm = BatchManager(self)
        for t in self.cotrainers:
            t._prepare_trainer(epochs=self.epochs, cycle=self.cycle)
            t._cycle_init()

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            for i in range(self.epochs):
                with self.co_train_mode:
                    for self.batch, batch in enumerate(self.train_Xy_cpu):
                        self.batch = (self.batch + 1) % len(self.train_dl)
                        #print(f"batch {batchnr} n {self._cycle_n} epoch {self.epochid} next {self.record_next_epoch}")
                        self.bm.prepare_batch(batch)
                        for t in self.alltrainers:
                            if t.check_scheduler and t.scheduler._step_count == t.scheduler.total_steps:
                                t.del_scheduler()
                                t.scheduler # create a new scheduler
                            t.batch = self.batch
                            *X, y = self.bm.get_batch_gpu(t)
                            t.optimizer.zero_grad()
                            y_pred = t.model(*X)
                            loss = t.loss(y_pred, y)
                            loss.backward()
                            t.optimizer.step()
                            t.scheduler.step()
                            if self.currentpbar:
                                self.currentpbar.update(self.train_dl.batch_size)

                            if self.record_this_epoch:
                                y_pred = t.post_forward(y_pred)
                                t.evaluator.accumulate_train_metrics(y, y_pred.detach(), loss.detach())

                        if self._check_end_of_cycle(self.batch):
                            with self.co_eval_mode:
                                self._co_validate(self.bm)
                                if self._conf_test:
                                    self._co_test(self.bm)
                                for t in self.alltrainers:
                                    t._train_finish()
                                    t._validate_finish()
                                    if self._conf_test:
                                        t._test_finish()
                                    t._cycle_init()
                                    t._check_save()
                                self._report_cycle()
                                if self._check_early_termination():
                                    return

    def _train_one_batch(self, *X, y, record=True, pbar=None):
        if self.check_scheduler and self.scheduler._step_count == self.scheduler.total_steps:
            self.del_scheduler()
            self.scheduler # create a new scheduler
        loss, y_pred = self._train_batch(*X, y=y)
        self.scheduler.step()

        try:
            if pbar is not False:
                if pbar is None:
                    self.currentpbar.update(self.train_dl.batch_size)
                else:
                    pbar.update(self.train_dl.batch_size)
        except: pass
        #print(self.epochid, record_next_epoch, batch, record_batches)
        if record:
            y_pred = self.post_forward(y_pred)
            if self._debug:
                self.lastypfw = y_pred                          
            self.evaluator.accumulate_train_metrics(y, y_pred.detach(), loss.detach())

    def _co_validate(self, bm):
        for batchnr, batch in enumerate(self.valid_Xy_cpu):
            bm.prepare_batch(batch)
            for t in self.alltrainers:
                *X, y = bm.get_batch_gpu(t)
                y_pred = t.model(*X)
                loss = t.loss(y_pred, y)
                y_pred = t.post_forward(y_pred)
                t.evaluator.accumulate_valid_metrics(y, y_pred, loss)
                if self.currentpbar:
                    self.currentpbar.update(self.valid_dl.batch_size)

    def _co_test(self, bm):
        for batchnr, batch in enumerate(self.test_Xy_cpu):
            bm.prepare_batch(batch)
            for t in self.alltrainers:
                *X, y = bm.get_batch_gpu(t)
                y_pred = t.model(*X)
                loss = t.loss(y_pred, y)
                y_pred = t.post_forward(y_pred)
                t.evaluator.accumulate_test_metrics(y, y_pred, loss)
                if self.currentpbar:
                    self.currentpbar.update(self.test_dl.batch_size)
            
    @property
    def record_this_epoch(self):
        return self.record_next_epoch == self.epochid + 1
    
    def _check_end_of_cycle(self, batchnr):
        if batchnr in self.record_batches:
            if self.record_next_epoch == self.epochid + 1 and batchnr == 0:
                if batchnr == 0:
                    for t in self.alltrainers:
                        t.epochid += 1
                    self.record_next_epoch = self.epochid + self.cycle if self.cycle >= 1 else self.epochid + 1
                return True
            elif self.record_next_epoch == self.epochid + 1 and batchnr > 0:
                return True
        if batchnr == 0:
            for t in self.alltrainers:
                t.epochid += 1

 
    def _prepare_trainer(self, lr=None, epochs=None, cycle=None, 
              optimizer=None, scheduler=False, 
              weight_decay=None, betas=None, 
              save_lowest=None, silent=None, pbar=None,
              targetloss=None, targettrainloss=None, earlystop=None, 
              validate=None, annotation=None, test=None, gpu=None):
        self.terminated = False
        self.silent = silent or self.silent
        self.lowest_validloss = None
        self.cycle = cycle or self.cycle
        assert epochs is not None or type(self) == CoTrainer, 'You must specify the number epochs for this trainer'
        self.epochs = epochs or self.epochs
        self._conf_validate = validate or self._conf_validate
        self._conf_test = test or self._conf_test
        self._conf_validate_annotation = annotation or self._conf_validate_annotation
        self._conf_earlystop = earlystop or self._conf_earlystop
        self._conf_save_lowest = save_lowest or self._conf_save_lowest
        self.targetloss = targetloss or self.targetloss
        self.targettrainloss = targettrainloss or self.targettrainloss
        self._scheduler_start = self.epochid # used by OneCycleScheduler
        self._scheduler_epochs = self.epochs
        assert lr is not None or self.lr is not None, 'You must specify a learning rate'
        self.lr = lr or self.lr
        self.del_optimizer()
        self.weight_decay = weight_decay or self.weight_decay
        self.betas = betas or self.betas
        if optimizer and self._optimizer_class != optimizer:
            self.optimizer = optimizer
        if scheduler is not False:
            self.scheduler = scheduler
        if gpu is not None:
            self.gpu(gpu)
        self._cyclesnotimproved = 0
        self._lastvalidation = None
        #torch.set_grad_enabled(False)
        self.maxepoch = self.epochid + self.epochs
        self._epochspaces = int(math.log(self.maxepoch)/math.log(10)) + 1
        self.pbar = pbar or self.pbar
        self._session_closepbar = self.pbar is None
        if self.pbar is None:
            if test:
                self.currentpbar = tqdm_trainer(len(self.alltrainers),
                                                self.epochs, 
                                                self.cycle, 
                                                self.train_dl, 
                                                self.valid_dl, 
                                                self.test_dl, 
                                                silent=self.silent)
            else:
                self.currentpbar = tqdm_trainer(len(self.alltrainers),
                                                self.epochs, 
                                                self.cycle, 
                                                self.train_dl, 
                                                self.valid_dl, 
                                                silent=self.silent)
        else:
            self.currentpbar = self.pbar
        self._time()
        self.check_scheduler = self.scheduler.__class__ == OneCycleLR
        if self.cycle < 1:
            self.record_batches = np.linspace(1, len(self.train_dl), int(round(1 / self.cycle))+1)[:-1]
            self.record_batches = { int(round(b))-1 for b in self.record_batches }
        else:
            self.record_batches = { 0 }
        self.record_next_epoch = self.epochid + self.cycle if self.cycle > 1 else self.epochid + 1
   
    def _check_save(self):
        loss = self._last_valid_metrics['loss']
        if self.lowest_validloss is None or loss < self.lowest_validloss:
            self.lowest_validloss = loss
            if self._conf_save_lowest:
                self.commit('lowest')
            
    def _report_cycle(self):
        if not self.silent:
            reportmetric = ''
            for m in self.metrics:
                m = m.__name__
                value = self._last_valid_metrics[m]
                try:
                    reportmetric += f'{m}={value:.5f} '
                except: pass
            print(f'{self.epochidstr} {self._time():.2f}s trainloss={self._last_train_metrics["loss"]:.5f} validloss={self._last_valid_metrics["loss"]:.5f} {reportmetric}')
   
    def _check_early_termination(self):
        validloss = self._last_valid_metrics['loss']
        trainloss = self._last_train_metrics['loss']
        if self.targetloss is not None and validloss <= self.targetloss:
            try:
                self.currentpbar.finish_fold()
            except: pass
            if not self.silent:
                print(f'Early terminating because the validation loss {validloss} reached the target {self.targetloss}.')
            self.terminated = True
        if self.targettrainloss is not None and trainloss <= self.targettrainloss:
            try:
                self.currentpbar.finish_fold()
            except: pass
            if not self.silent:
                print(f'Early terminating because the train loss {trainloss} reached the target {self.targettrainloss}.')
            self.terminated = True
        if self._conf_earlystop:
            if self._lastvalidation is None:
                self._lastvalidation = validloss
                self.commit('earlystop')
            else:
                if validloss < self._lastvalidation:
                    self._cyclesnotimproved = 0
                    self.commit('earlystop')
                else:
                    self._cyclesnotimproved += 1
                    if self._cyclesnotimproved >= earlystop:
                        self.purge('earlystop')
                        try:
                            self.currentpbar.finish_fold()
                        except: pass
                        if not self.silent:
                            if earlystop == 1 or earlystop == True:
                                print(f'Early terminating because the validation loss has not improved the last cycle.')
                            else:
                                print(f'Early terminating because the validation loss has not improved the last {earlystop} cycles.')
                        self.terminated = True
        return self.terminated

    def lowest(self):
        """
        Checkout the model with the lowest validation loss, that was committed when training with save_lowest=True
        """
        self.checkout('lowest')

    def debug(self):
        if self._debug:
            try:
                print('last X', self.lastx)
            except: pass
            try:
                print('last y', self.lasty)
            except: pass
            try:
                print('last model(X)', self.lastyfw)
            except: pass
            try:
                print('last post_forward(model(X))', self.lastypfw)
            except: pass
        
    def learning_curve(self, y='loss', series='phase', select=None, xlabel = None, ylabel = None, title=None, label_prefix='', fig=plt, legendargs={}, **kwargs):
        """
        Plot a learning curve with the train and valid loss on the y-axis over the epoch on the x-axis. 
        The plot is generated by the evaluator that recorded training progress. By default the evaluator records:
        - epoch: the epoch number
        - phase: 'train', 'valid' or 'test'
        - model: the model name is taken from the label of the trainer
        - loss: the weighted average loss
        under the name of each metric function, the resulting value when called with (y, y_pred)
        and the additional values that are passed to train() through the annotation parameter. 
        
        Arguments:
            y: str or function
                the metric that is used for the y-axis. It has to be a metric that was collected during training.
                if a function is passed, the name of the function is used.
            series: str ('phase')
                the label to use as a series. By default, 'phase' is used to plot both the train and valid results.
            select: see evaluator.select
                using the values 'train' and 'valid' you can select to plot only the train or valid sets.
            xlabel: str
                the label used on the x-axis
            ylabel: str
                the label used on the y-axis
            title: str
                the title of the plot
            label_prefix: str
                prefixes the label, so that you can combine a plot with results from different metrics or models
            legendargs: dict ({})
                arguments that are passed to legend
            **kwargs: dict
                forwarded to matplotlib's plot or scatter function
        """
        return self.evaluator.line_metric(x='epoch', series=series, select=select, y=y, xlabel = xlabel, ylabel = ylabel, title=title, label_prefix=label_prefix, fig=fig, **kwargs)
        
    def validation_curve(self, y=None, x='epoch', series='phase', select=None, xlabel = None, ylabel = None, title=None, label_prefix=None, fig=plt, **kwargs):
        """
        Plot a metric for the train and valid set, over epoch on the x-axis. The plot is generated by the evaluator
        that recorded training progress. By default the evaluator records:
        - epoch: the epoch number
        - phase: 'train', 'valid' or 'test'
        - loss: the weighted average loss
        - model: as given by the label of the trainer
        under the name of each metric function, the resulting value when called with (y, y_pred)
        and the additional values that are passed to train() through the annotation parameter. 
        
        Arguments:
            y: str or function
                the metric that is used for the y-axis. It has to be a metric that was collected during training.
                if a function is passed, the name of the function is used.
            x: str ('epoch')
                the label used for the x-axis.
            series: str ('phase')
                series will be used to group the data with Pandas, and plot a curve for each value.
                By default, 'phase' is used to plot both the train, valid and/or test results.
            select: str|dict see evaluator.select (None)
                using the values 'train' and 'valid' you can select to plot only the train or valid sets.
            xlabel: str
                the label used on the x-axis
            ylabel: str
                the label used on the y-axis
            title: str
                the title of the plot
            label_prefix: str
                prefixes the label, so that you can combine a plot with results from different metrics or models
            fig: pyplot.Figure (None)
                the figure to put the plot in
            **kwargs: dict
                forwarded to matplotlib's plot or scatter function
        """
        label_prefix = label_prefix or self.label + ' '
        if y is not None and type(y) != str:
            y = y.__name__
        return self.evaluator.line_metric(x=x, series=series, select=select, y=y, xlabel = xlabel, ylabel = ylabel, title=title, label_prefix=label_prefix, fig=fig, **kwargs)
       
    def curves(self, x='epoch', series='phase', select=None, xlabel = None, title=None, label_prefix=None, **kwargs):
        m = len(self.metrics) + 1
        fig, ax = plt.subplots(nrows=1, ncols=m, figsize=(6 * m, 4))
        if title is not None:
            fig.title(title)
        for i, y in enumerate(['loss'] + self.metrics):
            self.validation_curve(y=y, x=x, series=series, select=select, xlabel=xlabel, label_prefix=label_prefix, fig=ax[i], **kwargs)
        
    def freeze(self, last=-1):
        """
        Mostly used for transfer learning, to freeze all parameters of a model, until the given layer (exclusive).
        
        Arguments:
            last: int (-1)
                Freeze all layers up to this layer number. -1 is the last layer.
        """
        for c in list(self.model.children())[:last]:
            for p in c.parameters():
                p.requires_grad=False

    def unfreeze(self):
        """
        Mostly used for transfer learning, to unfreeze all parameters of a model.
        """
        for c in list(self.model.children()):
            for p in c.parameters():
                p.requires_grad=True

    def study(self, *target, storage=None, sampler=None, pruner=None, 
              study_name=None, direction=None, load_if_exists=False, 
              directions=None, grid=None):
        """
        Creates an (extended) Optuna Study to study how hyperparameters affect the given target function 
        when training a model. This call will just instantiate and return the study object. Typical use is to
        first define a `trial` function, that will sample values to use as hyperparameters, instantiate and train a model,
        and return the optimal validation scores using `trainer.optimum`. Then call `study.optimize(trail, n_trials=)`
        to run the trial n_trial times. You can use `tuner.plot_hyperparameters()` to visualize the results, or any
        optuna method.
        
        If you want to create a study without optimizing for loss first, `Study.create_study` allows you to
        set the targets and directions.
        
        Arguments:
            grid: dict (None)
                dictionary with the values to use in a grid search
        
            for the arguments, see create_study in the Optuna library
            
        Returns:
            Study (which is a subclass of Optuna.study.Study)
        """
        from ..evaluate.study import Study
        return Study.create_study(*target, storage=storage, 
                                  sampler=sampler, pruner=pruner, 
                                  study_name=study_name, direction=direction, 
                                  load_if_exists=load_if_exists, directions=directions, 
                                  grid=grid)
    
    def metrics_optimum(self, *target, direction=None, directions=None, **select):
        """
        Finds the cycle at which optimal results where obtained over the validation set, on the given optimization
        metric. 
        
        Args:
            *target: str or callable ('loss')
                names or metric functions that are used to decide what training cycle the model was most optimal

            direction: str or [ str ] (None)
                for every target: 'minimize' or 'maximize' to find the highest or lowest value on the given target
                If None, 'minimize' is used when optimize is 'loss', otherwise 'maximize' is used
 
            directions: [ str ] (None)
                same as direction, but now a list of 'minimize' or 'maximize' for multipe targets.
            
            select: {} (None)
                When None, the annotations from the last call to record_metric are used (which is often
                the last annotation generated from train()). 
                
                Otherwise, select is a dictionary with values that distinguish the results from the 
                current trial to the previous trails, which is needed to find the single best epoch 
                of the current trail to return the metrics for that epoch.
                
        Returns:
            { targetname:value }
            A dictionary of target values 
        """
        if len(target) == 0:
            target = ['loss'] + [ m.__name__ for m in self.metrics ]
        else:
            target = [ t.__name__ if callable(t) else t for t in target ]
            for t in target:
                try:
                    assert t == 'loss' or t in { m.__name__ for m in self.metrics }, \
                        f'Target {t} should be loss or a metric that is registered for the trainer'
                except:
                    assert False, f'Exception comparing target {t} to the registered metrics of the trainer'
        if direction is None and directions is None:
            if len(target) > 1:
                directions = [ 'minimize' if t == 'loss' else 'maximize' for t in target ]
            else:
                direction = 'minimize' if target[0] == 'loss' else 'maximize'
        return self.evaluator.metrics_optimum(*target, direction=direction, directions=directions, **select)

    def metrics_optimum_multi(self, *target, direction=None, directions=None, **select):
        return [ t.metrics_optimum( *target, direction=direction, directions=directions, **select)
                 for t in self.alltrainers ]
    
    def optimum(self, *target, direction=None, directions=None, **select):
        """
        Finds the cycle at which optimal results where obtained over the validation set, on the given optimization
        metric. 
        
        Args:
            *target: str or callable ('loss')
                names or metric functions that are used to decide what training cycle the model was most optimal

            direction: str or [ str ] (None)
                for every target: 'minimize' or 'maximize' to find the highest or lowest value on the given target
                If None, 'minimize' is used when optimize is 'loss', otherwise 'maximize' is used
 
            directions: [ str ] (None)
                same as direction, but now a list of 'minimize' or 'maximize' for multipe targets.
            
            select: {} (None)
                When None, the annotations from the last call to record_metric are used (which is often
                the last annotation generated from train()). 
                
                Otherwise, select is a dictionary with values that distinguish the results from the 
                current trial to the previous trails, which is needed to find the single best epoch 
                of the current trail to return the metrics for that epoch.
                
        Returns:
            [ target ]
            A list of target values 
        """
        if len(target) == 0:
            target = ['loss'] + [ m.__name__ for m in self.metrics ]
        else:
            target = [ t.__name__ if callable(t) else t for t in target ]
            for t in target:
                try:
                    assert t == 'loss' or t in { m.__name__ for m in self.metrics }, \
                        f'Target {t} should be loss or a metric that is registered for the trainer'
                except:
                    assert False, f'Exception comparing target {t} to the registered metrics of the trainer'
        if direction is None and directions is None:
            if len(target) > 1:
                directions = [ 'minimize' if t == 'loss' else 'maximize' for t in target ]
            else:
                direction = 'minimize' if target[0] == 'loss' else 'maximize'
        return self.evaluator.optimum(*target, direction=direction, directions=directions, **select)
    
    def optimum_multi(self, *target, direction=None, directions=None, **select):
        return [ t.optimum(*target, direction=direction, directions=directions, **select) 
                 for t in self.alltrainers ]
    
    def plot_hyperparameters(self, figsize=None):
        self.tuner.plot_hyperparameters(figsize)
        
    def lr_find(self, lr=[1e-6, 10], steps=40, smooth=0.05, cache_valid=True, interactive=False, **kwargs):
        """
        Run a learning rate finder on the dataset (as propesed by Leslie Smith and implemented in FastAI). 
        This saves the model, then starting with a very low learning rate
        iteratively trains the model on a single mini-batch and records the loss on the validation set. Gradually, the
        learning rate is raised. The idea is that the graph contains information on a stable setting of the learning
        rate. This does not always work, and often after some training, if learning is not stable, the learning rate
        still needs to bstee adjusted. 
        
        The result is a plot of the validation loss over the change in learning rate.
        
        Arguments:
            lr: [small float, big float] ([1e-6, 10])
                Interval of learning rates to inspect
                
            steps: int (40)
                number of (exponential) steps to divide the learning rate interval in
                
            smooth: float (0.05)
                smoothing parameter, to generate a more readable graph
                
            cache_valid: bool (True)
                whether to keep the validation set if possible in memory. Switch of if there is insufficient memory
                
            interactive: bool (False)
                switches the backend to matplotlib notebook to show the plot during training and switches
                to matplotlib inline when it is done. It cannot (yet) detect the previous backend, so this
                will only work when inline is the default mode.
        """
        if interactive:
            run_magic('matplotlib', 'notebook')
        with tuner(self, exprange(lr[0], lr[1], steps), self.set_lr, label='lr', yscale='log', smooth=smooth, cache_valid=cache_valid, **kwargs) as t:
            t.run()
        if interactive:
            run_magic('matplotlib', 'inline')
    
class BatchManager:
    """
    This is a helper class for training multiple models on multiple GPU's, by broadcasting the data
    towards the GPU cards.
    """
    
    def __init__(self, lead, expected_memory_needed=1000, expected_load=0.05):
        self.lead = lead
        self.all = lead.alltrainers
        self.expected_memory_needed = expected_memory_needed
        self.expected_load = expected_load
        self.reset_gpus()
        self.assign_devices()

    @property
    def trainers_auto_gpu(self):
        r = [ c for c in self.all if c._gpu == True ]
        r = sorted(r, key=lambda t: -t.model_size)
        return r

    @property
    def trainers_pre_assigned_gpu(self):
        r = [ c for c in self.all if type(c._gpu) == int ]
        return r

    def get_gpu_info(self):
        try:
            import GPUtil
        except:
            assert False, 'You must install GPUtil to use gpu=True'
        return GPUtil.getGPUs()

    def update_gpus(self):
        try:
            del self._gpus
        except: pass
        return self.gpus

    @property
    def gpus(self):
        try:
            self._gpus
        except:
            self._gpus = self.get_gpu_info()
        return self._gpus
        
    @property
    def sorted_gpus(self):
        r = sorted(self.gpus, key=lambda x: self.expectedLoad[x.id])
        r = list(filter(lambda x: self.expectedMem[x.id] > 1000 + self.expected_memory_needed, r))
        return r
    
    def show_gpus(self_):
        return pd.DataFrame([(g.id, g.load, g.memoryFree) for g in self.gpus], 
                            columns=['id', 'load', 'memFree'])
        
    def reset_gpus(self):
        self.expectedLoad = {}
        self.originalMem = {}
        self.originalLoad = {}
        self.expectedMem = {}
        self.memoryAssigned = {}
        self.trainersAssigned = {}
        for gpu in self.gpus:
            self.originalMem[gpu.id] = gpu.memoryFree
            self.originalLoad[gpu.id] = gpu.load
            self.expectedMem[gpu.id] = gpu.memoryFree
            self.expectedLoad[gpu.id] = gpu.load
            self.memoryAssigned[gpu.id] = 0
            self.trainersAssigned[gpu.id] = 0

    def assign_device(self, trainer, gpu):
        trainer._device = torch.device(f'cuda:{gpu}')
        self.trainersAssigned[gpu] += 1
        self.expectedMem[gpu] -= self.required_mem(trainer)
        self.expectedLoad[gpu] += self.expected_load

    def required_mem(self, trainer):
        return trainer.model_size * 3 / 1000000
        
    def assign_devices(self):
        warned = False
        trainers = self.trainers_auto_gpu
        c = Counter()
        i = 0
        for t in self.trainers_pre_assigned_gpu:
            self.assign_device(t, t.gpu)
        gpus = self.sorted_gpus
        try:
            for i, t in enumerate(trainers):
                gpu = gpus[i % len(gpus)]
                if not self.expectedMem[gpu.id] > self.required_mem(t):
                    if warn == False:
                        warn = true
                        print('''
    We may run out of GPU resources, if that happens you can try to:
    - analyze the expected optimal amount of trainers by running with just 
    one cotrainer for a single cycle
    - reduce the number of cotrainers, batch_size and/or the size of your models
    - free up memory by closing notebooks
    ''')
                self.assign_device(t, gpu.id)
        except:
            raise MemoryError
            
    @property
    def assigned_gpus(self):
        return { t.device.index for t in self.all if t.device.type == 'cuda' or  t.device.type == 'xla' }

    @property
    def assigned_devices(self):
        try:
            return self._assigned_devices
        except:
            self._assigned_devices = { t.device for t in self.all if t.device.type == 'cuda' or t.device.type == 'xla' }
            return self._assigned_devices

    def prepare_batch(self, batch):
        *self.X, self.y = batch
        self._batch_gpu = {}

    def get_batch_gpu(self, trainer):
        gpu = trainer.device.index
        try:
            return self._batch_gpu[gpu]
        except:
            self._batch_gpu = { id:[] for id in self.assigned_gpus }
            #print(X, y)
            for i in range(len(self.X)):
                distributed_tensors = broadcast(self.X[i], devices=self.assigned_devices)
                #print(distributed_tensors)
                for tens in distributed_tensors:
                    id = tens.device.index
                    self._batch_gpu[id].append(tens)
            distributed_tensors = broadcast(self.y, devices=self.assigned_devices)
            for tens in distributed_tensors:
                id = tens.device.index
                self._batch_gpu[id].append(tens)
            #print(self._batch_gpu)
            return self._batch_gpu[gpu]
        
    def __len__(self):
        return len(self.y)
        
    def analyze_usage(self):
        self.update_gpus()
        trainers_assigned = sum([ g.trainersAssigned for g in self.gpus ])
        totalMemNeeded = sum([ g.memoryFree - g.originalMem for g in self.gpus if g.trainers_assigned > 0 ])
        avgMemNeeded = totalMemNeeded / trainers_assigned
        nonMaxLoad = count([ g for g in self.gpus if g.load < 0.9 ])
        avgLoadNeeded = sum([ g.load - g.originalLoad for g in self.gpus ]) / nonMaxLoad
        self.expected_memory_needed = avgMemNeeded 
        self.expected_load = avgLoadNeeded

    def report(self):
        self.analyze_usage()
        m = 0
        totalMemFree = 0
        totalLoad = 0
        for g in self.gpus:
            acceptable_load = round(1 - g.originalLoad) / self.expected_load
            acceptable_mem = (g.originalMem) // self.avgMemNeeded
            m += min(accpetable_load, acceptable_mem)
            totalMemFree += g.originalMem
            totalLoad += g.originalLoad
        devices = count(self.gpus)

        print(f"""
Expected optimal number of concurrent trainers that can be used. 
Important considerations:
- the expected optimum is computed for a single user, when you expect that during
  your training sessions other users are also likely to start training, please use
  less resources. The server will then be faster for everyone.
- it is not possible to estimate the optimum use for tasks that already used the GPU
  since claimed memory will not be released until a task is terminated. Therefore, to
  get a good prediction for the optimal setting you have to restart your entire 
  notebook and run the training analyzer before any other actions on the GPU card.
- the analysis is affected by other users, if conditions change, the suggested settings
  are no longer optimal.

At the start of the analysis there was a total load of {totalLoad} available over 
{devices} devices with a total amount of {totalMemFree} free memory. On average a session
used {self.avgLoadNeeded} x 100% load from a GPU and {self.avgMemNeeded} memory.

The recommendation is to leave gpu=True and use no more than {m} concurrent trainers 
in total.
""")
            
class CoTrainer(Trainer):
    """
    A Trainer that trains together with another trainer for efficient training.
    
    Using multiple GPU cores for training a single model often does not scale well
    with the increase of resources. The efficiency of training multiple models on 
    the same device is often limited by disk I/O. The idea of co-trainers, is that
    multiple models that need te same dataset can be trained more efficiently in a 
    single session by using a single data pipeline. The pipeline is provided by a
    "lead" trainer, and when training this lead trainer it will pass data onto 
    "co" trainers to train on the same data feed.
    
    The first argument here is the lead trainer, from which the data source is shared.
    For the remainder, every training can be configured independently, with a few small
    exceptions. On co-trainers, quiet mode is always on and when gpu=true devices will be
    assigned by the lead trainer to spread the workload over the available resources.
    
    Arguments:
        model: nn.Module
            a PyTorch Module that will be trained
            
        loss: callable
            a PyTorch or custom loss function
            
        metrics: callable or list of callable
            One or more functions that can be called with (y, y_pred)
            to compute an evaluation metric. This will automatically be
            done during training, for both the train and valid sets.
            Typically, the callable is a function from SKLearn.metrics
            like mean_squared_error or recall_score.
            
        optimizer: PyTorch Optimizer or str (AdamW)
            The P_yTorch or custom optimizer CLASS (not an instance!) that is 
            used during training.
            
            You can either provide:
            - an optimizer CLASS from the torch.optim module,
            - a custom optimizer CLASS that obeys the same API, 
            - a partial of an optimizer CLASS with optimization arguments set
            - 'AdamW', 'Adam', 'RMSprop', 'Adadelta', 'Adagrad', 'Adamax', 
              'LBFGS', 'SGD', or 'SparseAdam'
                        
        scheduler: None, OneCycleLR, ConstantLR
            used to adapt the learning rate: 
            - None will use a constant learning rate
            - OneCycleLR will will use a cyclic annealing learning rate
              between an upper and lower bound.
            - ConstantLR will use a linear decaying learning rate between
              an upper bound and lower bound. You can optionally use
              'cycle' when calling 'train' to restart ConstantLR 
              every 'cycle' epochs.
              
        weight_decay: float
            When set, the trainer will attempt to instantiate an optimizer
            with weight_decay set. When the optimizer does not support weight
            decay, it will fail.
            
        betas: float
            When set, the trainer will attempt to instantiate an optimizer
            with betas set. When the optimizer does not support betas it will fail.
            
        random_state: int
            used to set a random state for reproducible results
            
        gpu: bool, int or torch.device (True)
            By default ths is set to True, because this simply makes most sense for running 
            multiple trainers simultaneously.
            
        post_forward: func (None)
            For some projects, the loss function requires a different output than
            the metrics that are being used. 

            Example 1: For nn.BCELoss() the target value
            must be a likelihood, while accuracy_score requires a class label. 
            The model returns a likelihood with an nn.Sigmoid() on the ouput layer, 
            but the metrics can only be computed if the likelihood is converted into 
            a predicted label (e.g. torch.round() ). 

            Example 2: nn.CrossEntropyLoss() requires a distribution over the possible labels
            while multci-class evaluation matrics require the predicted class. This is commonly
            computed with torch.argmax(y, dim=1).

            To allow for this behavior, the trainer can use a post_forward fuction inbetween
            loss and metrics. It will attempt to use a post_forward in the following order: 
            - a function passed here
            - a post_forward method that is added to the model
            - infer a post_forward based on the loss function. 

            For inferring a post_forward based on
            the loss function, there is a dictionary in train.POST_FORWARD that covers the 
            most commonly used loss functions.

            If no post_forward is found, and the loss function is unknown, then None is used
            and a warning is printed. Pass post_forward=False to suppress this warning.
            
        silent: bool (True)
            Be default, CoTrainers are silenced
            
        debug: bool (False)
            stores X, y and y_pred in properties so that they can be inspected
            when an error is thrown.
    """
    def __init__(self,
                 lead,
                 model, 
                 loss, 
                 metrics = None, 
                 optimizer='AdamW', 
                 scheduler=None, 
                 weight_decay=None, 
                 betas=None, 
                 gpu=True,
                 random_state=None, 
                 debug=False,
                 silent=True,
                 post_forward=None,
                 lr=None,
                 cycle=None,
                 save_lowest=False, 
                 pbar=None,
                 label=None,
                 annotation=None
                ):
  
        assert lr is not None, 'You have to supply a complete training configuration including a learning rate for CoTrainers'
            
        self.cotrainer_number = len(lead.cotrainers)+1
        super().__init__(model, loss, train_dl=lead.train_dl, valid_dl=lead.valid_dl, test_dl=lead.test_dl,
                         metrics=metrics, optimizer=optimizer, 
                        scheduler=scheduler, weight_decay=weight_decay, betas=betas,
                        gpu=gpu, random_state=random_state,
                        debug=debug, silent=silent, post_forward=post_forward, 
                        lr=lr, cycle=cycle, save_lowest=save_lowest,
                        annotation=annotation, halt_notebook=False)
        self.evaluator = lead.evaluator.share(self, lead.evaluator, label=self.label)
        self.lead = lead
        lead.register_cotrainer(self)
        
    @property
    def _conf_validate_annotation(self):
        return self.__conf_validate_annotation or self.lead._conf_validate_annotation
        
    @_conf_validate_annotation.setter
    def _conf_validate_annotation(self, value):
        self.__conf_validate_annotation = value
        try:
            del self.__validate_annotation
        except: pass
    
    @property
    def label(self):
        try:
            if self._label is not None:
                return self._label
        except: pass
        return f"{self.model.__class__.__name__}_co{self.cotrainer_number}"
        
    @label.setter
    def label(self, value):
        self._label = value
            
