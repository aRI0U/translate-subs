from collections import Counter
from pprint import pprint
from tqdm import tqdm

import numpy as np

from split.score import ClauseSplitter


def tune_model(config):
    splitter = ClauseSplitter("fr_dep_news_trf", **config)
    counter = Counter()
    with open("data/newline_dataset.txt", 'r') as f:
        for line in tqdm(f.readlines(), total=38352):
            try:
                sep_idx = line.index(r'\N')
            except ValueError:
                print(line)
                print("No escape")
                continue
            sentence = line.replace(r'\N', ' ').strip()
            indices = splitter.compute_split_indices(sentence, ratio=0.5)
            try:
                rank = np.where(indices == sep_idx)[0][0]
            except IndexError:
                print(line)
                print(indices, sep_idx)
                continue
            counter[rank] += 1
    pprint(counter)


if __name__ == "__main__":
    tune_model({})
