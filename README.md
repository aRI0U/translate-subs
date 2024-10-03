# Subtitles processor

A Python library for processing subtitles files automatically.

**Disclaimer:** I may work again on this project one day but to be honest it will probably be dropped. It should still work though. Feel free to use it, redistribute it and/or submit PR/issues if you find it useful. 🙂

## Functionalities

This library has originally been written to automatically translate subtitles, but additional functionalities have been 
added:
- Auto-translation
- Detection of tags in subtitles and possibility to remove them/keep them after translation
- Warning when the text of the subtitle is too long for its duration (too high CPS)
- Put `\N` symbols at the right place when subtitles are quite long
- Handle multi-subtitles sentences to get a better long-term consistency in translations

If you think of additional features, do not hesitate to send an issue! PRs are also more than welcome!

## Setup

- Install Python 3 and the requirements (see below)
- Clone this repository

### Mandatory requirements

- Python 3 (tests have been done with Python 3.8 but it might work with older versions)
- [pysubs2](https://pysubs2.readthedocs.io/en/latest/) (can be installed with `pip`)

### Optional requirements

Additional Python libraries should be installed to be able to use all the features of this library:
- [NumPy](https://numpy.org/) and [spaCy](https://spacy.io/) for using the clause splitter (for translating long sentences or adding new line symbols automatically)
- [tqdm](https://github.com/tqdm/tqdm) or [rich](https://rich.readthedocs.io/en/stable/progress.html) to have nice progress bars
- [Ray Tune](https://docs.ray.io/en/latest/tune/index.html) for searching good sets of hyperparameters for the clause splitter (advanced usage)

All these libraries can be installed with `pip`. Other imports within the code are from the standard library.


## Usage

1. In the `config` directory, create your configuration file to specify the language to translate from/to, 
   eventual callbacks and clause splitter with their respective parameters, etc.
   You can take inspiration from the config files that are already provided.
2. If you want to use the DeepL auto-translation feature, subscribe to DeepL API.
   With the free version, you can translate up to 500 000 characters per month. Then, copy-paste your token in a text file 
   called `tokens.txt`. If you have more than one account, you can put several tokens there.
3. The program can be run from a terminal. To run it, just type the following and indicate the path to the subtitles 
   file(s) you want to translate:
   ```commandline
   python3 main.py -c /path/to/my/config.yaml <subfile1.ass> <subfile2.ass> ...
   ```

Instead of writing the path of the subtitles files in the command, you can write them in a text file 
and provide the path to the text file in the command with option `-f`.
By default, processed subtitles files are written in a folder called `processed/`. You can override this behaviour
with option `--outfile-pattern`.

Type `python3 main.py --help` for more details about the different options.


## Code organization

The repository is organized as follows:

### `callbacks`

Callbacks are specific functions that are called on each subtitles just before/after translating them.
Pre/post-processing operations (e.g. tag handling, new line symbols) are therefore implemented here.

Each callback has two methods: `on_before_translate` and `on_after_translate`.
Each of them takes a subtitle event as argument and returns it eventually modified, so you can have access on the text,
style, duration and every useful information about the subtitle in the methods.

In particular, the order of callbacks might be significant. Given a list of callbacks `c1, c2, ..., cn`, the
`on_before_translate` method is called in the order of the list but then the `on_after_translate` is called in **the 
reverse order**.

You can also implement your own callbacks by subclassing the base class `Callback`, e.g. if you want to parse specific 
tags to replace them by custom styles or anything you might think of. Just take inspiration from the already provided 
ones for implementing your owns. Moreover, if you think your callback could be beneficial to someone else, do not 
hesitate to submit a pull request.

### `config`

To avoid having to write too long commands, the proposed solutions for handling the (numerous) parameters of the script 
is `yaml` config files, as they are easy to parse by both humans and machines.

Parameters of the eventual translator and splitter can be indicated directly in the `yaml` file.
In particular, the `backend` argument corresponds to the name of the file in which the `Translator` you want to use is 
implemented (in practice there is only `deepl` so you do not have to care about it right now).

Callbacks are indicated as a list. For callbacks that do not have any argument, you can just indicate the name of the 
callback. For ones that have some, you should pass a dictionary whose first key is `callback_name` (provide the 
name of the corresponding callback here) and `callback_args` (provide all args as a dictionary here).
**Recall that the order of callbacks may change the behavior of the program.**

Examples of config files are already provided in folder `config`, do not hesitate to take inspiration from them.

### `data`

This scripts are not called within the main one but are utils to create datasets out of true subtitles files.
This is useful for fine-tuning splitter hyperparameters but should be let to advanced users.

### `glossaries`

This folder contains glossaries as JSON files that are then fed to the `Translator` to increase the quality of the 
generated translations. It is particularly useful when there are some specific words or expressions in the show whose 
translation is not the usual one. It can also be used to appropriately translate characters' names.

Just write your glossary in this folder and then indicate its path to the translator in your configuration file.

An example is provided in folder `glossaries`.

### `split`

This module contains the implementation of the `Splitter` class, which splits whole sentences into relevant clauses.
It therefore enables to improve the translations of sentences split across multiple events and automatically write the
`\N` symbols.

In fact, proper splitting of subtitles is an absolutely non-trivial task. Let's take the following sentence:
***I finally managed to get out of jail thanks to the princess.***

This sentence is definitely too long to be displayed on a single line of subtitles. It therefore has to be split.
VLC would split it automatically however in practice it is a good practice to indicate where the line break should be.

In fact, the following split
<p style="text-align: center;">I finally managed to get out of jail<br>thanks to the princess.</p>
is more comfortable to read and makes more sense than this one:
<p style="text-align: center;">I finally managed to get out of<br>jail thanks to the princess.</p>

And yet, the number of words/letters is more balanced in the second split.
This example reveals that one cannot only rely on *numeric* features to split a subtitle but also has to consider 
*syntactic* features, which makes the task much harder to automate.

The algorithm used by the splitter uses a combination of the following approaches to solve this task:
- A pre-trained Transformer model outputs the graph of relations between the different words within a sentence.
- A loss enforces the split to be balanced, i.e. both lines should have roughly the same length.
- Deterministic penalties avoid subtitles to be split e.g. just before a punctuation sign or just after a determinant.

The weights of these different approaches are computed in a data-driven way, i.e. so that the split accuracy over a 
dataset of subtitles is maximal (see **Performances**).

### `translate`

TODO

### `utils`

TODO

## Performances

### Translator

The quality of the translations depends on the underlying API, I cannot do anything if the translations are bad...

In practice, translations from French to English seem to be quite clean. It is of course not as perfect as a 
professional translation but it is a strong that only requires minor corrections.

However, translating from English to French often lead to quite poor results, mostly because French is more specific 
than English, enforcing the translator to do arbitrary choices (for example "you" can be translated by "tu" or "vous" 
depending on the context). The resulting subs are usually understandable and you can follow a show using them if you do
not have any other solution, but honestly you should do this only as a last resort. For releasing purposes, the 
auto-translated subtitles can be a good starting point but a lot of manual corrections would probably have to be done.

I did not try to use other source/target languages, but I assume that the conclusions would be similar.

**Warning:** As far as I know, DeepL only translates from/to English, so if you want to translate e.g. from French to 
Spanish it will translate first French to English then English to Spanish, leading to less accurate translations.

The quality of the translations on long sentences could be improved using the `ClauseSplitter` with an appropriate set 
of hyperparameters. Work in progress...



### Splitter

Hyperparameters of the clause splitter have been chosen to match the manual splits of a dataset of subtitles.

#### Dataset details

- **Dataset name:** FR_DC
- **Source:** Detective Conan E0761-1037 FR subs (Crunchyroll)
- **Dataset size:** 15945 lines (train), 990 lines (test)
- **Good hyperparameters:**

  - `alpha`: 1e-4
  - `det`: 3.0
  - `punct`: -2.0
  - `power_syntactic`: 1.5
  - `power_positional`: 4.5

- **Performances:**

| alpha | det | punct | power_syntactic | power_positional | top1_acc_train | top1_acc_test | top3_acc_train | top3_acc_test |
|:-----:|:---:|:-----:|:---------------:|:----------------:|:--------------:|:-------------:|:--------------:|:-------------:|
| 1e-4  | 3.0 | -2.0  |       1.5       |       4.5        |     87.5%      |     88.6%     |     97.5%      |     98.3%     |

  - Top-1 accuracy: 70.9%

  - Top-3 accuracy: 93.3%

## Contributing

Pull requests are more than welcome!

### Translator

As of now, the only `Translator` that has been implemented uses the [DeepL](https://www.deepl.com/docs-api) API, 
which has been shown to have good performances in translation.
If you want to implement another translator, just implement it as a subclass of `translate.base.Translator` and 
implement the `translate_text` method. Then add your custom translator in `translate.__init__.py` and you should be 
able to call it by specifying the appropriate backend in your config file (see **Usage**).

### Callbacks

To implement your own callbacks, create a new file in `callbacks/` and create a subclass of the ABC `Callback`.
Your callback will be automatically registered to the package, so that you would be able to call it by typing 
`callbacks.MySuperCallback` after module `callbacks` is imported. Similarly, the callback can be called directly 
by name in your config file.

## TODO

### Short-term

- finish writing `README.md`
- finish to find good hyperparameters

### Long-term

- informative and proper logging using `logging` instead of `print`/`warnings`
- more informative progress bar when using `rich`
- check if the set of hparams is the same in all languages
- more permissive outfile-pattern
- detail the behaviour of splitter and callbacks
- handle `TODOs` everywhere in the code
- explain how to tune hyperparameters by oneself
- finish to write docs
- argparser for `tune_hparams.py` and `data/prepare_data.py`

### "Future work"

- Add other translators
- make the README look professional
- GUI
- nice name and logo
- make it installable with `pip`
