import re

from pysubs2 import SSAEvent

from .base import Callback


class TagEraserCallback(Callback):
    def __init__(self):
        super(TagEraserCallback, self).__init__()
        self.tag_regex = re.compile(r"{[^}]*}")

    def on_before_translate(self, event: SSAEvent) -> SSAEvent:
        event.text = self.tag_regex.sub("", event.text)
        return event
