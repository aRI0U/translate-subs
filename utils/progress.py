import warnings

PROGRESS_LIB = None
try:
    from rich.progress import track
    PROGRESS_LIB = "rich"
    PROGRESS_FN = track
except (ImportError, ModuleNotFoundError):
    try:
        from tqdm import tqdm
        PROGRESS_LIB = "tqdm"
        PROGRESS_FN = tqdm
    except (ImportError, ModuleNotFoundError):
        pass


def progress_bar(sequence, **kwargs):
    if PROGRESS_LIB == "rich":  # TODO: customize rich progress bar
        return track(sequence, **kwargs)

    if PROGRESS_LIB == "tqdm":
        kwargs["desc"] = kwargs.pop("description")
        return tqdm(sequence, **kwargs)

    warnings.warn("To display nice progress bars, please install `rich` or `tqdm` first.")
    desc = kwargs.get("description")
    if desc:
        print(desc)
    return sequence
