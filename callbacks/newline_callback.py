import warnings

from pysubs2 import SSAEvent

from split.splitter import ClauseSplitter
from .base import Callback


class NewlineCallback(Callback):
    r"""Put a `\N` at a relevant place if the subtitle is too long to be in one line. The relevant place is determined
    by an internal `ClauseSplitter`.

    Args:
        limit_length (int): Maximal length for one-line subtitles
        *args, **kwargs: Arguments of the internal clause splitter
    """
    def __init__(self, limit_length: int = 36, *args, **kwargs):
        super(NewlineCallback, self).__init__()
        self.splitter = ClauseSplitter(*args, **kwargs)
        self.limit_length = limit_length

    def on_after_translate(self, event: SSAEvent) -> SSAEvent:
        text = event.text
        if self.should_not_be_split(text):  # avoid more than two lines per subtitle
            return event

        indices = self.splitter.compute_split_indices(text, ratio=0.5)
        if len(indices) == 0:  # very unlikely since it would mean sub is a single super-long word
            warnings.warn("A super-long word has been detected, that may be an error: " + text)
            return event

        idx = indices[0]
        event.text = text[:idx] + r"\N" + text[idx+1:]  # text[idx] is a space and new line + space would be redundant
        return event

    def should_not_be_split(self, text: str) -> bool:
        r"""Indicates whether the text of the subtitle should be split into two lines or not

        Args:
            text (str): text of the subtitle

        Returns:
            bool: whether it should be split
        """
        return len(text) <= self.limit_length or r'\N' in text
