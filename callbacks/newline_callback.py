from split.score import ClauseSplitter
from .base import Callback


class NewlineCallback(Callback):
    def __init__(self, *args, **kwargs):
        super(NewlineCallback, self).__init__()
        self.splitter = ClauseSplitter(*args, **kwargs)

    def on_after_translate(self, text: str) -> str:
        indices = self.splitter.compute_split_indices(text, ratio=0.5)
        idx = indices[0]
        return text[:idx] + r"\N" + text[idx:]
