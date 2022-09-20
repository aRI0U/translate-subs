import abc
from pysubs2 import SSAEvent


class Callback(abc.ABC):
    def on_before_translate(self, event: SSAEvent) -> SSAEvent:
        return event

    def on_after_translate(self, event: SSAEvent) -> SSAEvent:
        return event
