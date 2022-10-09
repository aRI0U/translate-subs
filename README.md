# Subtitles processor

...

## Functionalities

## Setup

This library needs

## Usage

## Code organization

## Splitter performance

Hyperparameters of the clause splitter have been chosen to match the manual splits of a dataset of subtitles.

### Details for new line dataset

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


## TODO

### Short-term

- write `README.md`
- add docs at least for callbacks
- put a licence
- finish to find good hyperparameters
- write a `requirements.txt`
- ensure minimal imports

### Long-term

- better logging
- better progress bar when using `rich`
- check if the set of hparams is the same in all languages
- more permissive outfile-pattern

### "Future work"

- Add other translators
- make the README look professional
- GUI
- nice name and logo
- make it installable with `pip`
