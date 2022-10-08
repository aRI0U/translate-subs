import warnings

PROGRESS_FN = None
try:
    from rich.progress import track
    PROGRESS_FN = track
except (ImportError, ModuleNotFoundError):
    try:
        from tqdm import tqdm
        PROGRESS_FN = tqdm
    except (ImportError, ModuleNotFoundError):
        pass


def progress_bar(sequence, **kwargs):
    if PROGRESS_FN is not None:
        return PROGRESS_FN(sequence, **kwargs)

    warnings.warn("To display nice progress bars, please install `rich` or `tqdm` first.")
    desc = kwargs.get("description")
    if desc:
        print(desc)
    return sequence
