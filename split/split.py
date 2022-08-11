import spacy
import deplacy
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


query = u"Tout d'abord, vers 8h30, M. Torakura s'est rendu au bureau " \
        u"et Tadokoro, Ran et Conan sont allés chercher un film dans " \
        u"la salle de collecte, c'est-à-dire juste derrière eux."
# query = u"First, at around 8:30, Mr. Torakura went to the study and Tadokoro, Ran, and Conan went to the collection room to get a film."
nlp = spacy.load("fr_dep_news_trf")
# nlp = spacy.load("en_core_web_trf")
doc = nlp(query)
deplacy.render(doc)

sent = next(doc.sents)
print(type(sent))
s = SyntaxicScore()
scores = s.compute(sent)

for token, score in zip(sent, scores):
    print(token, "\n\t", score)
