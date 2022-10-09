from .base import Translator


def import_translator(backend: str) -> Translator:
    if backend == "deepl":
        from .deepl import DeepLTranslator
        return DeepLTranslator
    raise ValueError(f"Invalid backend selected. Valid choices are `deepl`, but found `{backend}`.")
