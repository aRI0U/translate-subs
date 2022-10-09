import abc


class Translator(abc.ABC):
    def __init__(
            self,
            source_lang: str,
            target_lang: str
    ):
        self.source_lang = source_lang
        self.target_lang = target_lang

    @abc.abstractmethod
    def translate_text(self, text: str) -> str:
        pass
