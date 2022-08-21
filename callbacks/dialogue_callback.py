from .base import Callback


class DialogueCallback(Callback):
    def __init__(self):
        super(DialogueCallback, self).__init__()
        self.is_dialogue = None

    def on_before_translate(self, text: str) -> str:
        self.is_dialogue = r"\N-" in text
        return text

    def on_after_translate(self, text: str) -> str:
        if self.is_dialogue:
            text = text.replace(" -", r"\N-")
        return text
