import re

from pysubs2 import SSAEvent

from .base import Callback


class CPSWarningCallback(Callback):
    def __init__(self, max_cps: float = 21.):
        self.max_cps = max_cps
        self.regex = re.compile("\W*")

    def on_after_translate(self, event: SSAEvent) -> SSAEvent:
        letters_only = re.sub(self.regex, "", event.plaintext)
        cps = len(letters_only) / max(event.duration / 1000, 1e-5)
        if cps > self.max_cps:
            print(f"Warning: found an event with a CPS of {cps:.1f}: ", event)
        return event
