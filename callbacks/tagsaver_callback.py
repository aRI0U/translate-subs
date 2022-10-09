import warnings

from pysubs2 import SSAEvent

from .base import Callback


class TagSaverCallback(Callback):
    r"""Removes an eventual tag in the subtitle before translating it and put it back after translation.
    Works only if the tag is at the borders of the subtitle.
    """
    def __init__(self):
        super(TagSaverCallback, self).__init__()
        self.start_tag = None
        self.end_tag = None

    def on_before_translate(self, event: SSAEvent) -> SSAEvent:
        text = event.text
        end_start_tag = 0
        start_end_tag = len(text)

        if text.startswith('{'):
            end_start_tag = text.find('}') + 1
        if text.endswith('}'):
            start_end_tag = text.rfind('{')

        if end_start_tag == -1 or start_end_tag == -1:
            warnings.warn("Invalid parsing for this subtitle:" + text)
        else:
            self.start_tag = text[:end_start_tag]
            self.end_tag = text[start_end_tag:]
            text = text[end_start_tag: start_end_tag]

        event.text = text
        return event

    def on_after_translate(self, event: SSAEvent) -> SSAEvent:
        event.text = self.start_tag + event.text + self.end_tag
        return event
