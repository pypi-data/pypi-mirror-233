
from optuna.study._optimize import *
from optuna.study.study import *

def _optimize_batches(
    study: "optuna.Study",
    func: "optuna.study.study.ObjectiveFuncType",
    batch_size: int,
    n_trials: Optional[int] = None,
    timeout: Optional[float] = None,
    catch: Tuple[Type[Exception], ...] = (),
    callbacks: Optional[List[Callable[["optuna.Study", FrozenTrial], None]]] = None,
    gc_after_trial: bool = False,
    show_progress_bar: bool = False,
) -> None:
    if not isinstance(catch, tuple):
        raise TypeError(
            "The catch argument is of type '{}' but must be a tuple.".format(type(catch).__name__)
        )

    if study._thread_local.in_optimize_loop:
        raise RuntimeError("Nested invocation of `Study.optimize` method isn't allowed.")

    progress_bar = pbar_module._ProgressBar(show_progress_bar, n_trials, timeout)

    study._stop_flag = False

    try:
            _optimize_batch(
                study,
                func,
                batch_size,
                n_trials,
                timeout,
                catch,
                callbacks,
                gc_after_trial,
                reseed_sampler_rng=False,
                time_start=None,
                progress_bar=progress_bar,
            )
    finally:
        study._thread_local.in_optimize_loop = False
        progress_bar.close()


def _optimize_batch(
    study: "optuna.Study",
    func: "optuna.study.study.ObjectiveFuncType",
    batch_size: int,
    n_trials: Optional[int],
    timeout: Optional[float],
    catch: Tuple[Type[Exception], ...],
    callbacks: Optional[List[Callable[["optuna.Study", FrozenTrial], None]]],
    gc_after_trial: bool,
    reseed_sampler_rng: bool,
    time_start: Optional[datetime.datetime],
    progress_bar: Optional[pbar_module._ProgressBar],
) -> None:
    # Here we set `in_optimize_loop = True`, not at the beginning of the `_optimize()` function.
    # Because it is a thread-local object and `n_jobs` option spawns new threads.
    study._thread_local.in_optimize_loop = True
    if reseed_sampler_rng:
        study.sampler.reseed_rng()

    i_trial = 0

    if time_start is None:
        time_start = datetime.datetime.now()

    while True:
        if study._stop_flag:
            break

        if n_trials is not None:
            if i_trial >= n_trials:
                break
            i_trial += 1

        if timeout is not None:
            elapsed_seconds = (datetime.datetime.now() - time_start).total_seconds()
            if elapsed_seconds >= timeout:
                break

        try:
            # patch
            frozen_trials = _run_trial_batch(study, func, catch, batch_size)
        finally:
            # The following line mitigates memory problems that can be occurred in some
            # environments (e.g., services that use computing containers such as GitHub Actions).
            # Please refer to the following PR for further details:
            # https://github.com/optuna/optuna/pull/325.
            if gc_after_trial:
                gc.collect()

        if callbacks is not None:
            for callback in callbacks:
                # patch
                for frozen_trial in frozen_trials:
                    callback(study, frozen_trial)

        if progress_bar is not None:
            elapsed_seconds = (datetime.datetime.now() - time_start).total_seconds()
            progress_bar.update(elapsed_seconds, study)

    study._storage.remove_session()

def _run_trial_batch(
    study: "optuna.Study",
    func: "optuna.study.study.ObjectiveFuncType",
    catch: Tuple[Type[Exception], ...],
    batch_size: int
) -> trial_module.FrozenTrial:
    if is_heartbeat_enabled(study._storage):
        optuna.storages.fail_stale_trials(study)

    trials = [ study.ask() for i in range(batch_size) ]

    state: Optional[TrialState] = None
    value_or_values: Optional[Union[float, Sequence[float]]] = None
    func_err: Optional[Union[Exception, KeyboardInterrupt]] = None
    func_err_fail_exc_info: Optional[Any] = None

    # patch
    with get_heartbeat_thread(trials[0]._trial_id, study._storage):
        try:
            # patch
            values = func(trials)
            assert len(values) == len(trials), 'number of returned results must match number of trials'
            states = [ TrialState.Pruned if value is None else None for value in values ]
        except exceptions.TrialPruned as e:
            # TODO(mamu): Handle multi-objective cases.
            # patch
            assert False, 'You should not use TrialState.Pruned in concurrent mode, rather return None to prune'
            func_err = e
        except (Exception, KeyboardInterrupt) as e:
            # patch
            states = [ TrialState.FAIL ] * len(trials)
            func_err = e
            func_err_fail_exc_info = sys.exc_info()

    # `_tell_with_warning` may raise during trial post-processing.
    try:
        # patch
        frozen_trials = [ _tell_with_warning(
            study=study,
            trial=trial,
            value_or_values=value,
            state=state,
            suppress_warning=True,
            ) 
            for trial, value, state in zip(trials, values, states) ]
    except Exception:
        frozen_trial = study._storage.get_trial(trial._trial_id)
        raise
    finally:
        # patch
        for frozen_trial in frozen_trials:
            if frozen_trial.state == TrialState.COMPLETE:
                study._log_completed_trial(frozen_trial)
            elif frozen_trial.state == TrialState.PRUNED:
                _logger.info("Trial {} pruned. {}".format(frozen_trial.number, str(func_err)))
            elif frozen_trial.state == TrialState.FAIL:
                if func_err is not None:
                    _log_failed_trial(
                        frozen_trial,
                        repr(func_err),
                        exc_info=func_err_fail_exc_info,
                        value_or_values=value_or_values,
                    )
                elif STUDY_TELL_WARNING_KEY in frozen_trial.system_attrs:
                    _log_failed_trial(
                        frozen_trial,
                        frozen_trial.system_attrs[STUDY_TELL_WARNING_KEY],
                        value_or_values=value_or_values,
                    )
                else:
                    assert False, "Should not reach."
            else:
                assert False, "Should not reach."

    if (
        frozen_trial.state == TrialState.FAIL
        and func_err is not None
        and not isinstance(func_err, catch)
    ):
        raise func_err
    return frozen_trials

def optimize_batch(
    self,
    func: ObjectiveFuncType,
    n_trials: Optional[int] = None,
    timeout: Optional[float] = None,
    batch_size: int = 1,
    catch: Union[Iterable[Type[Exception]], Type[Exception]] = (),
    callbacks: Optional[List[Callable[["Study", FrozenTrial], None]]] = None,
    gc_after_trial: bool = False,
    show_progress_bar: bool = False,
) -> None:
    """Optimize an objective function.
    Optimization is done by choosing a suitable set of hyperparameter values from a given
    range. Uses a sampler which implements the task of value suggestion based on a specified
    distribution. The sampler is specified in :func:`~optuna.study.create_study` and the
    default choice for the sampler is TPE.
    See also :class:`~optuna.samplers.TPESampler` for more details on 'TPE'.
    Optimization will be stopped when receiving a termination signal such as SIGINT and
    SIGTERM. Unlike other signals, a trial is automatically and cleanly failed when receiving
    SIGINT (Ctrl+C). If ``n_jobs`` is greater than one or if another signal than SIGINT
    is used, the interrupted trial state won't be properly updated.
    Example:
        .. testcode::
            import optuna
            def objective(trial):
                x = trial.suggest_float("x", -1, 1)
                return x**2
            study = optuna.create_study()
            study.optimize(objective, n_trials=3)
    Args:
        func:
            A callable that implements objective function.
        n_trials:
            The number of trials for each process. :obj:`None` represents no limit in terms of
            the number of trials. The study continues to create trials until the number of
            trials reaches ``n_trials``, ``timeout`` period elapses,
            :func:`~optuna.study.Study.stop` is called, or a termination signal such as
            SIGTERM or Ctrl+C is received.
            .. seealso::
                :class:`optuna.study.MaxTrialsCallback` can ensure how many times trials
                will be performed across all processes.
        timeout:
            Stop study after the given number of second(s). :obj:`None` represents no limit in
            terms of elapsed time. The study continues to create trials until the number of
            trials reaches ``n_trials``, ``timeout`` period elapses,
            :func:`~optuna.study.Study.stop` is called or, a termination signal such as
            SIGTERM or Ctrl+C is received.
        batch_size:
            The number of trials that are passed to func simultaneously.
        catch:
            A study continues to run even when a trial raises one of the exceptions specified
            in this argument. Default is an empty tuple, i.e. the study will stop for any
            exception except for :class:`~optuna.exceptions.TrialPruned`.
        callbacks:
            List of callback functions that are invoked at the end of each trial. Each function
            must accept two parameters with the following types in this order:
            :class:`~optuna.study.Study` and :class:`~optuna.trial.FrozenTrial`.
            .. seealso::
                See the tutorial of :ref:`optuna_callback` for how to use and implement
                callback functions.
        gc_after_trial:
            Flag to determine whether to automatically run garbage collection after each trial.
            Set to :obj:`True` to run the garbage collection, :obj:`False` otherwise.
            When it runs, it runs a full collection by internally calling :func:`gc.collect`.
            If you see an increase in memory consumption over several trials, try setting this
            flag to :obj:`True`.
            .. seealso::
                :ref:`out-of-memory-gc-collect`
        show_progress_bar:
            Flag to show progress bars or not. To disable progress bar, set this :obj:`False`.
            Currently, progress bar is experimental feature and disabled
            when ``n_trials`` is :obj:`None`, ``timeout`` is not :obj:`None`, and
            ``n_jobs`` :math:`\\ne 1`.
    Raises:
        RuntimeError:
            If nested invocation of this method occurs.
    """

    _optimize_batches(
        study=self,
        func=func,
        n_trials=n_trials,
        timeout=timeout,
        batch_size=batch_size,
        catch=tuple(catch) if isinstance(catch, Iterable) else (catch,),
        callbacks=callbacks,
        gc_after_trial=gc_after_trial,
        show_progress_bar=show_progress_bar,
    )

Study.optimize_batch = optimize_batch
