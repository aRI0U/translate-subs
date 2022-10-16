import csv
import re
from pathlib import Path
from typing import List

import pysubs2
from tqdm import tqdm


def filter_subs_old(subs, out_file):
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


def filter_subs(
        subs: pysubs2.SSAFile,
        writer: csv.DictWriter,
        valid_styles: List[str],
        invalid_styles: List[str],
        manual: bool = False
):
    spaces_regex = re.compile(" +")

    for line in subs:
        # 1. filter non-valid subs
        try:
            if line.style not in valid_styles:
                if line.style in invalid_styles or line.plaintext.isupper():
                    continue

                if not manual:
                    invalid_styles.append(line.style)
                    continue

                print(line, f"Found an unseen style: {line.style}.")
                if input("Do you want this style to be parsed? [y/n]") == 'y':
                    valid_styles.append(line.style)
                else:
                    invalid_styles.append(line.style)
                    continue

            # 3. Correct invalid patterns
            text = re.sub(spaces_regex, " ", line.plaintext).replace('\n', r'\N').strip()
            if len(text) == 0:
                continue

            # Write the result
            writer.writerow({"start": line.start, "end": line.end, "text": text})
        except UnicodeDecodeError:
            continue

    return valid_styles, invalid_styles


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Prepare data for ")

    parser.add_argument("data_dir", type=Path, nargs='*', metavar="FILE",
                        help="TODO")
    parser.add_argument("-m", "--manual", action="store_true")
    parser.add_argument("--valid_styles", type=str, nargs='*')
    parser.add_argument("--invalid_styles", type=str, nargs='*')

    args = parser.parse_args()

    for p in args.data_dir:
        path = Path(p)
        raw_dir = path / "raw"
        csv_file = path / "filtered.csv"

        valid_styles = args.valid_styles or []
        invalid_styles = args.invalid_styles or []

        with open(csv_file, 'w', newline='') as f:
            fieldnames = ["start", "end", "text"]
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            pbar = tqdm(list(raw_dir.glob("*.ass")) + list(raw_dir.glob("*.srt")))
            for sub_file in pbar:
                pbar.set_description(f"Processing {sub_file}...")
                subs = pysubs2.load(sub_file)
                valid_styles, invalid_styles = filter_subs(
                    subs,
                    writer,
                    valid_styles=valid_styles,
                    invalid_styles=invalid_styles,
                    manual=args.manual
                )
        print(f"Valid styles ({len(valid_styles)}):")
        print(valid_styles)
        print(f"Invalid styles ({len(invalid_styles)}):")
        print(invalid_styles)
