from pysubs2 import SSAEvent

from .base import Callback


class DialogueCallback(Callback):
    def __init__(self):
        super(DialogueCallback, self).__init__()
        self.is_dialogue = None

    def on_before_translate(self, event: SSAEvent) -> SSAEvent:
        self.is_dialogue = r"\N-" in event.text
        return event

    def on_after_translate(self, event: SSAEvent) -> SSAEvent:
        if self.is_dialogue:
            event.text = event.text.replace(" -", r"\N-")
        return event
