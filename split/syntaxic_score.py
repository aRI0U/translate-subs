import spacy
import numpy as np


class SyntaxicScore:
    def __init__(self):
        self.scores = None

    def compute(self, sentence):
        self.scores = np.zeros(len(sentence) - 1)
        self._compute(sentence.root)
        return self._clean_scores(sentence, self.scores)

    def _compute(self, token):
        for left in token.lefts:
            self.scores[left.i: token.i] += 1
            self._compute(left)
        for right in token.rights:
            self.scores[token.i: right.i] += 1
            self._compute(right)

    @staticmethod
    def _clean_scores(sentence, scores):
        for i in range(1, len(sentence) - 1):
            token = sentence[i]
            if token.is_punct:
                scores[i] = min(scores[i-1], scores[i])
                scores[i-1] = np.inf
        return scores
