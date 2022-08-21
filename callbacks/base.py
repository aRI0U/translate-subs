import abc


class Callback(abc.ABC):
    def on_before_translate(self, text: str) -> str:
        return text

    def on_after_translate(self, text: str) -> str:
        return text
