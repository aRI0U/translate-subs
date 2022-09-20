import csv
import re
from pathlib import Path
from tqdm import tqdm

import pysubs2


def filter_subs(subs, out_file):
    tag_regex = re.compile(r"{\\.*?}")
    spaces_regex = re.compile(" +")
    for line in subs:
        # 1. filter non-valid subs
        if line.style != "Default" or line.text.isupper():
            continue

        # 2. Remove tags
        text = re.sub(tag_regex, "", line.text.strip())

        # 3. Correct invalid patterns
        text = re.sub(spaces_regex, " ", text)
        text = text.replace(r" \N", r"\N")
        if text.endswith(r'\N'):
            text = text[:-2]

        # Write the result
        out_file.write(text + '\n')


def filter_subs2(subs, writer):
    spaces_regex = re.compile(" +")
    for line in subs:
        # 1. filter non-valid subs
        if line.style != "Default" or line.text.isupper():
            continue

        # 3. Correct invalid patterns
        text = re.sub(spaces_regex, " ", line.plaintext).replace('\n', ' ').strip()
        if len(text) == 0:
            continue

        # Write the result
        writer.writerow({"start": line.start, "end": line.end, "text": text})


if __name__ == "__main__":
    raw_dir = Path("raw/")
    csv_file = Path("filtered_subs.csv")

    with open(csv_file, 'w', newline='') as f:
        fieldnames = ["start", "end", "text"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        pbar = tqdm(list(raw_dir.glob("*.ass")))
        for sub_file in pbar:
            pbar.set_description(f"Processing {sub_file}...")

            subs = pysubs2.load(sub_file)

            filter_subs2(subs, writer)
