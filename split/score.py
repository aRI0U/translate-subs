from typing import Optional

import numpy as np

import spacy


class ClauseSplitter:
    def __init__(self, model: str = "en_core_web_trf"):
        self.syntactic_model = spacy.load(model)

        self.span = None
        self.syntactic_loss = None
        self.positional_loss = None

    def compute_span(self, sentence: str):
        doc = self.syntactic_model(sentence)
        return next(doc.sents)

    def compute_loss(self, sentence: str, span, ratio: Optional[float] = None):
        syntactic_loss = self.compute_syntactic_loss(sentence, span)

        if ratio is None:
            return syntactic_loss

        positional_loss = self.compute_positional_loss(sentence, ratio)
        positional_loss = self._expand_positional_loss()
        loss = syntactic_loss + positional_loss  # TODO: clean this

        return loss

    # SYNTACTIC LOSS
    def compute_syntactic_loss(self, sentence, span):
        self.syntactic_loss = np.zeros(len(span) - 1)
        self._compute_syntactic_loss(span.root)
        self.syntactic_loss = self._clean_syntactic_loss(sentence, span, self.syntactic_loss)
        return self.syntactic_loss

    def _compute_syntactic_loss(self, token):
        for left in token.lefts:
            self.syntactic_loss[left.i: token.i] += 1
            self._compute_syntactic_loss(left)
        for right in token.rights:
            self.syntactic_loss[token.i: right.i] += 1
            self._compute_syntactic_loss(right)

    @staticmethod
    def _clean_syntactic_loss(sentence, span, scores):
        for i in range(len(span) - 1):
            token = span[i]
            if sentence[token.idx + len(token)] != ' ':
                scores[i] = np.inf
        return scores

    # POSITIONAL LOSS
    def compute_positional_loss(self, sentence: str, ratio: float):
        spaces_indices = self._get_space_indices(sentence)
        self.positional_loss = np.abs(spaces_indices - ratio * len(sentence))
        return self.positional_loss

    @staticmethod
    def _get_space_indices(sentence: str) -> np.ndarray:
        spaces_indices = []
        for i, c in enumerate(sentence):
            if c == ' ':
                spaces_indices.append(i)
        return np.array(spaces_indices)

    def _expand_positional_loss(self):
        positional_loss = np.zeros_like(self.syntactic_loss) + np.inf
        j = 0
        for i, loss in enumerate(self.syntactic_loss):
            if not np.isinf(loss):
                positional_loss[i] = self.positional_loss[j]
                j += 1
        self.positional_loss = positional_loss
        return self.positional_loss


if __name__ == "__main__":
    splitter = ClauseSplitter("fr_dep_news_trf")
    query = u"Tout d'abord, vers 8h30, M. Torakura s'est rendu au bureau " \
            u"et Tadokoro, Ran et Conan sont allés chercher un film dans " \
            u"la salle de collecte, c'est-à-dire juste derrière eux."
    span = splitter.compute_span(query)

    loss = splitter.compute_loss(query, span, ratio=0.3)

    for t, c in zip(span, loss):  # splitter.syntactic_loss):
        print(t, '\n\t', c)
