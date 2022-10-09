from typing import List, Optional

import numpy as np

import spacy

POS = {
    "det": 90,
    "punct": 97
}


class ClauseSplitter:
    def __init__(
            self,
            model: str = "en_core_web_trf",
            alpha: float = 1e-4,
            power_syntactic: float = 2,
            power_positional: float = 4,
            **kwargs
    ):
        self.syntactic_model = spacy.load(model)

        self.alpha = alpha
        self.power_syntactic = power_syntactic
        self.power_positional = power_positional

        self.span = None
        self._syntactic_loss = None
        self.positional_loss = None

        self.penalties = {POS[k]: v for k, v in kwargs.items()}

    def compute_spans(self, sentence: str) -> List:
        doc = self.syntactic_model(sentence)
        return [span for span in doc.sents]

    def compute_loss(self, sentence: str, spans, ratio: Optional[float] = None):
        syntactic_loss = self.compute_syntactic_loss(sentence, spans)

        if ratio is None:
            return syntactic_loss

        positional_loss = self.compute_positional_loss(sentence, ratio, np.isinf(syntactic_loss))

        return syntactic_loss ** self.power_syntactic + self.alpha * positional_loss ** self.power_positional

    def compute_split_indices(self, sentence: str, ratio: Optional[float] = None) -> np.ndarray:
        spans = self.compute_spans(sentence)
        loss = self.compute_loss(sentence, spans, ratio=ratio)
        ranking = np.argsort(loss)

        all_indices = []
        for span in spans:
            after_token_indices = np.zeros(len(span), dtype=int)
            for i in range(len(span)):
                token = span[i]
                after_token_indices[i] = token.idx + len(token)

            all_indices.append(after_token_indices)

        all_indices = np.concatenate(all_indices)[:-1]
        return all_indices[ranking]

    # SYNTACTIC LOSS
    def compute_syntactic_loss(self, sentence, spans):
        num_tokens = sum(len(span) for span in spans)
        self._syntactic_loss = np.zeros(num_tokens)
        offset = 0

        for span in spans:
            self._compute_syntactic_loss(span.root)
            self._clean_syntactic_loss(sentence, span, offset=offset)
            offset += len(span)

        # loss =
        loss, self._syntactic_loss = self._syntactic_loss, None
        return loss[:-1]

    def _compute_syntactic_loss(self, token):
        for left in token.lefts:
            self._syntactic_loss[left.i: token.i] += 1
            self._compute_syntactic_loss(left)
        for right in token.rights:
            self._syntactic_loss[token.i: right.i] += 1
            self._compute_syntactic_loss(right)

    def _clean_syntactic_loss(self, sentence, span, offset=0):
        for i, token in enumerate(span):
            # make error infinite on invalid splits
            next_char_idx = token.idx + len(token)
            if next_char_idx >= len(sentence) or \
                    sentence[next_char_idx] != ' ' or \
                    next_char_idx + 1 < len(sentence) and sentence[next_char_idx+1] in '!?:;':
                self._syntactic_loss[i + offset] = np.inf

            # add eventual penalties
            self._syntactic_loss[i + offset] += self.penalties.get(token.pos, 0)

        # clip syntactic loss
        self._syntactic_loss = self._syntactic_loss.clip(min=0)

    # POSITIONAL LOSS
    def compute_positional_loss(self, sentence: str, ratio: float, inf_mask: np.ndarray):
        spaces_indices = self._get_space_indices(sentence)
        positional_loss = np.abs(spaces_indices - ratio * len(sentence))
        positional_loss = self._expand_positional_loss(positional_loss, inf_mask)
        return positional_loss

    @staticmethod
    def _get_space_indices(sentence: str) -> np.ndarray:
        spaces_indices = []
        for i, c in enumerate(sentence):
            if c == ' ':
                spaces_indices.append(i)
        return np.array(spaces_indices)

    @staticmethod
    def _expand_positional_loss(positional_loss, inf_mask):
        # TODO: compute this efficiently
        expanded_loss = np.full(inf_mask.shape, np.inf)
        j = 0
        for i, inf in enumerate(inf_mask):
            if not inf:
                expanded_loss[i] = positional_loss[j]
                j += 1
        return expanded_loss


if __name__ == "__main__":
    import deplacy

    # splitter = ClauseSplitter("fr_dep_news_trf", alpha=1e-2)
    # penalties = {90: 2, 97: -2}
    splitter = ClauseSplitter("en_core_web_trf", alpha=1e-4, power_syntactic=4, det=2, punct=-1)
    # query = u"Tout d'abord, vers 8h30, M. Torakura s'est rendu au bureau " \
    #         u"et Bernard, Ran et Conan sont allés chercher un film dans " \
    #         u"la salle de collecte, c'est-à-dire juste derrière eux."
    # query = u"Qu'est-ce que vous faîtes ici ?! Partez immédiatement !!!"
    # query = u"Hmmm... Je vois."
    query = "An umbrella with a towel could help to draw Riri, Fifi and Loulou on the beach!"
    doc = splitter.syntactic_model(query)
    deplacy.render(doc)

    indices = splitter.compute_split_indices(query, ratio=None)
    # print(query)
    for i, idx in enumerate(indices):
        print(i+1)
        print(query[:idx] + " / " + query[idx+1:])
