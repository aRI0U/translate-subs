import warnings

try:
    from .splitter import ClauseSplitter
except (ImportError, ModuleNotFoundError):
    warnings.warn("You must install `numpy` and `spacy` to use the clause splitter.")

warnings.warn("The right parameters for the splitter have not been computed yet. "
              "With wrong parameters the splitter will be more harmful than helpful.")
