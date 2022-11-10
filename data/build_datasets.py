import csv
from pathlib import Path
from random import random

from tqdm import tqdm


def build_newline_dataset(data_dir: Path, split_ratio: float = 0.9):
    subs_file = data_dir / "filtered.csv"
    train_file = data_dir / "newline_dataset_train.csv"
    valid_file = data_dir / "newline_dataset_valid.csv"
    num_train_samples, num_valid_samples = 0, 0

    with subs_file.open('r') as f_in:
        with train_file.open('w') as f_train:
            with valid_file.open('w') as f_valid:
                reader = csv.DictReader(f_in, fieldnames=["start", "end", "text"], delimiter=';')
                train_writer = csv.DictWriter(f_train, fieldnames=["ratio", "text"], delimiter=';')
                valid_writer = csv.DictWriter(f_valid, fieldnames=["ratio", "text"], delimiter=';')

                for row in tqdm(reader):
                    text = row["text"].replace(r' \N', r'\N').replace(r'\N ', r'\N').replace('  ', ' ').strip()
                    if r'\N' in text and r'\N-' not in text:
                        if random() < split_ratio:
                            train_writer.writerow({"ratio": 0.5, "text": text})
                            num_train_samples += 1
                        else:
                            valid_writer.writerow({"ratio": 0.5, "text": text})
                            num_valid_samples += 1

    print("Done.")
    print("Number of training samples:", num_train_samples)
    print("Number of validation samples:", num_valid_samples)


def mid_of_sentence(clause):
    return clause[0].islower() or clause[0] in "\"-"


def build_split_dataset(data_dir: Path, max_pause: int = 2000, split_ratio: float = 0.9):
    subs_file = data_dir / "filtered.csv"
    train_file = data_dir / "split_dataset_train.csv"
    valid_file = data_dir / "split_dataset_valid.csv"
    num_train_samples, num_valid_samples = 0, 0

    with subs_file.open('r') as f_in:
        with train_file.open('w') as f_train:
            with valid_file.open('w') as f_valid:
                reader = csv.DictReader(f_in, fieldnames=["start", "end", "text"], delimiter=';')
                train_writer = csv.DictWriter(f_train, fieldnames=["ratio", "text"], delimiter=';')
                valid_writer = csv.DictWriter(f_valid, fieldnames=["ratio", "text"], delimiter=';')

                clauses = []
                sentence_end = 0

                for row in tqdm(reader):
                    text = row["text"].replace(r'\N', ' ').replace(r'  ', ' ').strip()
                    start = int(row["start"])
                    end = int(row["end"])
                    duration = end - start

                    # we consider there cannot be a blank of more than 2 seconds inside a sentence
                    if start > sentence_end + max_pause:
                        clauses = []

                    if text[-1] not in ".?!\"":
                        clauses.append((duration, text))
                        sentence_end = end

                    elif len(clauses) >= 1:
                        clauses.append((duration, text))

                        durations, texts = zip(*clauses)
                        total_duration = sum(durations)
                        if total_duration == 0:
                            continue

                        for i in range(1, len(clauses)):
                            ratio = sum(durations[:i]) / total_duration
                            text = ' '.join(texts[:i]) + r'\N' + ' '.join(texts[i:])
                            if random() < split_ratio:
                                train_writer.writerow({"ratio": ratio, "text": text})
                                num_train_samples += 1
                            else:
                                valid_writer.writerow({"ratio": ratio, "text": text})
                                num_valid_samples += 1

                        clauses = []
    print("Done.")
    print("Number of training samples:", num_train_samples)
    print("Number of validation samples:", num_valid_samples)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("dataset", type=str, choices=["newline", "split"])
    parser.add_argument("data_dir", type=Path, nargs='*')

    args = parser.parse_args()

    if args.dataset == "newline":
        for path in args.data_dir:
            build_newline_dataset(path)
    else:
        for path in args.data_dir:
            build_split_dataset(path)
