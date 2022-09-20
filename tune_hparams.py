import csv
from collections import Counter

import numpy as np

import ray.tune as tune
from ray.tune import CLIReporter
from ray.tune.schedulers import ASHAScheduler
from ray.tune.suggest.optuna import OptunaSearch

from split.score import ClauseSplitter


def compute_accuracy(c: Counter):
    total = sum(c.values())
    top1_acc = c[0] / total
    top3_acc = (c[0] + c[1] + c[2]) / total
    return top1_acc, top3_acc


def tune_model_split(config):
    splitter = ClauseSplitter("fr_dep_news_trf", **config)
    counter = Counter()
    with open("/home/alain/Documents/projects/translate-subs/data/split_dataset2.csv", 'r') as f:
        reader = csv.DictReader(f, fieldnames=["ratio", "text"], delimiter=';')
        for i, row in enumerate(reader):
            text = row["text"]
            ratio = float(row["ratio"])
            try:
                sep_idx = text.index(r'\N')
            except ValueError:
                print(text)
                print("No escape")
                continue
            sentence = text.replace(r'\N', ' ').strip()
            indices = splitter.compute_split_indices(sentence, ratio=ratio)
            try:
                rank = np.where(indices == sep_idx)[0][0]
            except IndexError:
                print(text)
                print(indices, sep_idx)
                continue
            counter[rank] += 1
            if i % 1000 == 0:
                top1_acc, top3_acc = compute_accuracy(counter)
                tune.report(top1_acc=top1_acc, top3_acc=top3_acc)

    top1_acc, top3_acc = compute_accuracy(counter)
    tune.report(top1_acc=top1_acc, top3_acc=top3_acc)


def tune_model_newline(config):
    splitter = ClauseSplitter("fr_dep_news_trf", **config)
    counter = Counter()
    with open("/home/alain/Documents/projects/translate-subs/data/newline_dataset.txt", 'r') as f:
        for i, line in enumerate(f.readlines()):
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
            if i % 1000 == 0:
                top1_acc, top3_acc = compute_accuracy(counter)
                tune.report(top1_acc=top1_acc, top3_acc=top3_acc)

    top1_acc, top3_acc = compute_accuracy(counter)
    tune.report(top1_acc=top1_acc, top3_acc=top3_acc)


def find_optimal_hparams(grid=False):
    if grid:
        config = {
            "alpha": 1e-4,
            "power_syntactic": tune.grid_search([1, 2, 3, 4]),
            "power_positional": 4
        }
    else:
        config = {
            "alpha": tune.loguniform(1e-4, 1e-2),
            "power_syntactic": tune.randint(1, 5),
            "power_positional": tune.randint(1, 5)
        }
    metrics = {
        "top1_acc": "top1_acc",
        "top3_acc": "top3_acc"
    }

    scheduler = ASHAScheduler(
        metric="top1_acc",
        mode="max",
        max_t=100,
        grace_period=10,
        reduction_factor=3
    )

    reporter = CLIReporter(
        metric_columns=list(metrics.keys()),
        metric="top1_acc",
        mode="max",
        max_report_frequency=30,
        sort_by_metric=True
    )

    result = tune.run(
        tune_model_split,
        resources_per_trial={"cpu": 2, "gpu": 0},
        config=config,
        num_samples=1 if grid else 100,
        local_dir="./ray_results",
        progress_reporter=reporter,
        scheduler=scheduler,
        search_alg=None if grid else OptunaSearch(metric="top1_acc", mode="max")
    )

    best_trial = result.get_best_trial("top1_acc", "max", "last")
    print("Best trial config: {}".format(best_trial.config))
    print("Best trial final top-1 accuracy: {}".format(
        best_trial.last_result["top1_acc"]))
    print("Best trial final top-3 accuracy: {}".format(
        best_trial.last_result["top3_acc"]))


if __name__ == "__main__":
    find_optimal_hparams(grid=False)
