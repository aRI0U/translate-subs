import os.path
from typing import Optional, Sequence

from pysubs2 import SSAEvent, SSAFile

from callbacks.base import Callback
from translate import Translator
from split.score import ClauseSplitter
from utils.progress import progress_bar


class SubtitlesProcessor:
    def __init__(
            self,
            translator: Optional[Translator] = None,
            splitter: Optional[ClauseSplitter] = None,
            callbacks: Optional[Sequence[Callback]] = None,
            dialogue_limit: int = 2000
    ):
        self.translator = translator
        self.splitter = splitter
        self.callbacks = callbacks if callbacks is not None else []
        self.dialogue_limit = dialogue_limit

        self.current_file = None

        self.translate_text = self._translate_text if translator is not None else lambda x: x

    def process_subtitles(self, in_file: str, out_file: str):
        self.current_file = in_file

        subs = SSAFile.load(in_file)
        subs.sort()
        complete = False

        try:
            if self.splitter is None:
                processed_subs = self._process_subs_wo_split(subs)
            else:
                processed_subs = self._process_subs_w_split(subs)
            complete = True
        finally:
            # create output directory if needed
            dirname = os.path.dirname(out_file)
            os.makedirs(dirname, exist_ok=True)

            # if not finished, indicate that the translation has been aborted
            if not complete:
                out_file = out_file.replace(".ass", "-aborted.ass")

            # save output subs
            processed_subs.save(out_file)

    def _process_subs_wo_split(self, subs: SSAFile) -> SSAFile:
        new_subs = SSAFile()
        for event in progress_bar(subs, description=self.current_file):
            processed_event = self.process_event(event)
            new_subs.append(processed_event)
        return new_subs

    def _process_subs_w_split(self, subs: SSAFile) -> SSAFile:
        new_subs = SSAFile()
        clauses = []

        for event in progress_bar(subs, description=self.current_file):  # TODO: use next/iter to aboid testing len(clauses) all the time
            if len(clauses) > 0 and self.sentence_split(clauses[-1], event):
                new_subs.extend(self.process_events(clauses))
                clauses = []
            clauses.append(event)
        new_subs.extend(self.process_events(clauses))

        return new_subs

    def process_event(self, event: SSAEvent) -> SSAEvent:
        for callback in self.callbacks:
            event = callback.on_before_translate(event)

        event.text = self.translate_text(event.text)

        for callback in reversed(self.callbacks):
            event = callback.on_after_translate(event)

        return event

    def process_events(self, events: Sequence[SSAEvent]) -> Sequence[SSAEvent]:
        processed_event = self.process_event(self.merge_events(events))

        start, duration = processed_event.start, processed_event.duration
        text = processed_event.text

        idx_list = [0]
        for e in events[:-1]:
            ratio = (e.end - start) / duration
            indices = self.splitter.compute_split_indices(text, ratio=ratio)
            if len(indices) == 0:
                break
            idx_list.append(indices[0])
        idx_list.append(len(text))

        for i in range(len(idx_list)-1):
            idx1, idx2 = idx_list[i], idx_list[i+1]
            events[i].text = text[idx1:idx2]

        return events

    def _translate_text(self, text: str) -> str:
        return self.translator.translate_text(text.replace(r"\N", " "))

    def sentence_split(self, event1: SSAEvent, event2: SSAEvent) -> bool:
        if event1.plaintext[-1] in ".?!\"":
            return True
        if event2.plaintext[0].isupper():
            return event2.start - event1.end > self.dialogue_limit
        return event2.start - event1.end > 2*self.dialogue_limit

    @staticmethod
    def merge_events(events: Sequence[SSAEvent]) -> SSAEvent:
        return SSAEvent(
            start=events[0].start,
            end=events[-1].end,
            text=' '.join(e.text for e in events),
            style=events[0].style
        )
