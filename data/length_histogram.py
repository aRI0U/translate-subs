from collections import Counter

import matplotlib.pyplot as plt


oneline_counter = Counter()
twolines_counter = Counter()

with open("filtered_subs.txt", 'r') as f:
    for line in f.readlines():
        line = line.strip()
        if r'\N' in line:
            line = line.replace(r'\N', ' ')
            twolines_counter[len(line)] += 1
        else:
            oneline_counter[len(line)] += 1

plt.bar(oneline_counter.keys(), oneline_counter.values(), color='r', alpha=0.25)
plt.bar(twolines_counter.keys(), twolines_counter.values(), color='b', alpha=0.25)
plt.show()
