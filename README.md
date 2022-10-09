# Subtitles processor

...

## Functionalities

This library has originally been written to automatically translate subtitles, but additional functionalities have been 
added:
- Auto-translation
- Detection of tags in subtitles and possibility to remove them/keep them after translation
- Warning when the text of the subtitle is too long for its duration (too high CPS)
- Put `\N` symbols at the right place when subtitles are quite long
- Handle multi-subtitles sentences to get a better long-term consistency in translations

## Setup

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

Type `python main.py -h`. More details will come later.

## Code organization

...

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

#### Details for new line dataset

- **Source:** Detective Conan E0761-1037 FR subs (Crunchyroll)
- **Dataset size:** 38338 lines
- **Optimal hyperparameters:**
  *ongoing*

[//]: # (  - `alpha`: 1e-4)

[//]: # (  - `power_syntactic`: 2)

[//]: # (  - `power_positional`: 4)

[//]: # (- **Performances:**)

[//]: # (  - Top-1 accuracy: 70.9%)

[//]: # (  - Top-3 accuracy: 93.3%)

## Contributing

Pull requests are more than welcome!

### Translator

As of now, the only `Translator` that has been implemented uses the [DeepL](https://www.deepl.com/docs-api) API, 
which has been shown to have good performances in translation.
If you want to implement another translator, just implement it as a subclass of `translate.base.Translator` and 
implement the `translate_text` method. Then add your custom translator in `translate.__init__.py` and you should be 
able to call it by specifying the appropriate backend in your config file (see **Usage**).

## TODO

### Short-term

- write `README.md`
- put a licence
- finish to find good hyperparameters
- write a `requirements.txt`
- ensure minimal imports
- put the splitter warning somewhere else
- help in parser

### Long-term

- informative and proper logging using `logging` instead of `print`
- more informative progress bar when using `rich`
- check if the set of hparams is the same in all languages
- more permissive outfile-pattern
- detail the behaviour of splitter and callbacks
- auto-register callbacks (decorator?)
- handle `TODOs` everywhere in the code
- explain how to tune hyperparameters by oneself
- finish to write docs

### "Future work"

- Add other translators
- make the README look professional
- GUI
- nice name and logo
- make it installable with `pip`
