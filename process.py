from pathlib import Path
from tqdm import tqdm
from typing import Optional, Sequence, Union

import pysubs2

from callbacks.base import Callback
from translate import Translator
from split.score import ClauseSplitter


class SubtitlesProcessor:
    def __init__(
            self,
            translator: Optional[Translator] = None,
            splitter: Optional[ClauseSplitter] = None,
            callbacks: Optional[Sequence[Callback]] = None
    ):
        self.translator = translator
        self.splitter = splitter
        self.callbacks = callbacks if callbacks is not None else []

        self.translate_text = self._translate_text if translator is not None else lambda x: x

    def process_subtitles(self, in_file: Union[Path, str], out_file: Union[str, Path]):
        subs = pysubs2.load(in_file)

        try:
            if self.splitter is None:
                processed_subs = self._process_subs_wo_split(subs)
            else:
                processed_subs = self._process_subs_w_split(subs)
        finally:
            processed_subs.save(out_file)

    def _process_subs_wo_split(self, subs):
        for line in tqdm(subs):
            line.text = self.process_text(line.text, line.style)

    def _process_subs_w_split(self, subs):
        pass

    def process_text(self, text: str, style):
        for callback in self.callbacks:
            text = callback.on_before_translate(text)

        text = self.translate_text(text)

        for callback in reversed(self.callbacks):
            text = callback.on_after_translate(text)

        return text

    def _translate_text(self, text):
        return self.translator.translate_text(text.replace(r"\N", " "))
