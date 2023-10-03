from functools import wraps

def is_documented_by(original, replace={}):
    @wraps(original)
    def wrapper(target):
        docstring = original.__doc__
        for key, value in replace.items():
            docstring = docstring.replace(key, value)
        target.__doc__ = docstring
        return target
    return wrapper

def run_magic(magic, line, cell=None):
    from IPython import get_ipython
    ipython = get_ipython()
    if cell is None:
        ipython.run_line_magic(magic, line)
    else:
        ipython.run_cell_magic(magic, line, cell)

        
def optuna_quiet_mode(self, quiet=True):
    """
    A ContextManager to silence optuna
    """
    class CM(object):
        def __enter__(self):
            if quiet:
                self.old_verbosity = optuna.logging.get_verbosity()
                optuna.logging.set_verbosity(optuna.logging.ERROR)

        def __exit__(self, type, value, traceback):
            if quiet:
                optuna.logging.set_verbosity(self.old_verbosity)

    return CM()

