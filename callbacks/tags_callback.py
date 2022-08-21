import warnings

from .base import Callback


class TagsCallback(Callback):
    def __init__(self):
        self.start_tag = None
        self.end_tag = None

    def on_before_translate(self, text: str) -> str:
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

        return text

    def on_after_translate(self, text: str) -> str:
        return self.start_tag + text + self.end_tag
