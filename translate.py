import logging
import json
from typing import Optional

import deepl


class NoTokensLeftException(Exception):
    pass


class Translator:
    def __init__(
            self,
            source_lang: str,
            target_lang: str,
            tokens_file: str,
            glossary: Optional[str] = None
    ):
        self.source_lang = source_lang
        self.target_lang = target_lang

        with open(tokens_file, 'r') as f:
            self._tokens_queue = [token.strip() for token in f.readlines()]

        self._init_translator()

        self._glossary = self._init_glossary(glossary) \
            if glossary is not None \
            else None

    def translate_text(self, text: str):
        while True:
            try:
                return self._translate_text(text).text
            except deepl.exceptions.DeepLException:
                logging.info(
                    "A DeepL exception occured: "
                    "restarting the translator with another token."
                )
                self._init_translator()

    def _init_translator(self):
        try:
            print(self._tokens_queue)
            self._translator = deepl.Translator(self._tokens_queue.pop())
        except IndexError:
            logging.exception(
                "Quota for this billing period has been exceeded, "
                "message: Quota Exceeded for all tokens."
            )
            raise NoTokensLeftException

    def _init_glossary(self, glossary: str):
        fname = glossary.split('/')[-1]
        name, ext = fname.rsplit('.', 1)
        if ext not in ["json"]:
            raise ValueError(
                "Invalid format of data detected. "
                "The only valid formats for glossary are: json."  # TODO: make it general
                f"But got format {ext}"
            )
        with open(glossary, 'r') as f:
            entries = json.load(f)
        print(name, self.source_lang, self.target_lang, entries)
        return self._translator.create_glossary(
            name,
            source_lang=self.source_lang,
            target_lang=self.target_lang,
            entries=entries
        )


    def _translate_text(self, text):
        if self._glossary is None:
            return self._translator.translate_text(text, source_lang=self.source_lang, target_lang=self.target_lang)
        return self._translator.translate_text_with_glossary(
            text,
            glossary=self._glossary
        )
