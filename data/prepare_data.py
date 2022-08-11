import re
from pathlib import Path
from tqdm import tqdm

import pysubs2


def filter_subs(subs, out_file):
    tag_regex = re.compile(r"{\\.*?}")
    for line in subs:
        # 1. filter non-valid subs
        if line.style != "Default" or line.text.isupper():
            continue

        # 2. Remove tags
        text = re.sub(tag_regex, "", line.text)

        # Write the result
        out_file.write(text + '\n')


if __name__ == "__main__":
    raw_dir = Path("raw/")
    txt_file = Path("filtered_subs.txt")

    with txt_file.open('w') as f:
        pbar = tqdm(list(raw_dir.glob("*.ass")))
        for sub_file in pbar:
            pbar.set_description(f"Processing {sub_file}...")

            subs = pysubs2.load(sub_file)

            filter_subs(subs, f)
