# Subtitles processor

A Python library for processing subtitles files automatically.

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

You can also implement your own callbacks by subclassing the base class `Callback`, e.g. if you want to parse specific 
tags to replace them by custom styles or anything you might think of. Just take inspiration from the already provided 
ones for implementing your owns. Moreover, if you think your callback could be beneficial to someone else, do not 
hesitate to submit a pull request.

### `config`

TODO

### `data`

TODO

### `glossaries`

TODO

### `split`

TODO

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
