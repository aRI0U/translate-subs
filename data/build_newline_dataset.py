import csv
from collections import defaultdict
from tqdm import tqdm


def build_newline_dataset():
    with open("filtered_subs.txt", 'r') as f:
        with open("newline_dataset.txt", 'w') as out:
            for line in f.readlines():
                if r"\N" in line and not r"\N-" in line:
                    out.write(line)


def mid_of_sentence(clause):
    return clause[0].islower() or clause[0] in "\"-"


def build_split_dataset_old():
    with open("filtered_subs.txt", 'r') as f:
        with open("split_dataset.txt", 'w') as out:
            clauses = []
            for i, line in enumerate(f.readlines()):
                if r"\N-" in line:
                    continue
                line = line.replace(r'\N', ' ').strip()
                if len(line) == 0:
                    continue
                if line[-1] not in ".?!\"":
                    # if len(clauses) > 0:
                    #     if not mid_of_sentence(line) and i > 6260:
                    #         print(f"Tried to append '{line}' after {clauses} (line {i+1:d})")
                    #         if input("[y/n] ").lower() != "y":
                    #             clauses = []
                    clauses.append(line)
                elif len(clauses) >= 1:
                    clauses.append(line)
                    out.write(r'\N'.join(clauses) + '\n')
                    clauses = []


def build_split_dataset():
    with open("filtered_subs.csv", 'r') as f_in:
        with open("split_dataset.csv", 'w') as f_out:
            reader = csv.DictReader(f_in, fieldnames=["duration", "text"], delimiter=';')
            writer = csv.DictWriter(f_out, fieldnames=["ratio", "text"], delimiter=';')

            clauses = []
            for row in tqdm(reader):
                text = row["text"].strip()
                duration = int(row["duration"])

                if text[-1] not in ".?!\"":
                    clauses.append((duration, text))

                elif len(clauses) >= 1:
                    clauses.append((duration, text))

                    durations, texts = zip(*clauses)
                    total_duration = sum(durations)
                    for i in range(1, len(clauses)):
                        ratio = sum(durations[:i]) / total_duration
                        text = ' '.join(texts[:i]) + r'\N' + ' '.join(texts[i:])
                        writer.writerow({"ratio": ratio, "text": text})

                    clauses = []


if __name__ == "__main__":
    # build_newline_dataset()
    build_split_dataset()
