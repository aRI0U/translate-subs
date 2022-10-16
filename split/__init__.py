try:
    from .splitter import ClauseSplitter
except (ImportError, ModuleNotFoundError):
    # define dummy class to raise error only when the class is instantiated
    class ClauseSplitter:
        def __init__(self, *args, **kwargs):
            raise ModuleNotFoundError("Please install `numpy` and `spacy` to use the clause splitter.")
