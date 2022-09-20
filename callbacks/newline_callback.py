from pysubs2 import SSAEvent

from split.score import ClauseSplitter
from .base import Callback


class NewlineCallback(Callback):
    def __init__(self, limit_length, *args, **kwargs):
        super(NewlineCallback, self).__init__()
        self.splitter = ClauseSplitter(*args, **kwargs)
        self.limit_length = limit_length

    def on_after_translate(self, event: SSAEvent) -> SSAEvent:
        text = event.text
        if len(text) <= self.limit_length:
            return event
        indices = self.splitter.compute_split_indices(text, ratio=0.5)
        if len(indices) == 0:  # very unlikely since it would mean sub is a single super-long word
            return event
        idx = indices[0]
        event.text = text[:idx] + r"\N" + text[idx:]
        return event
