## Performances

Hyperparameters of the clause splitter have been chosen to match the manual splits of a dataset of subtitles.

### Details for new line dataset

- **Source:** Detective Conan E0761-1037 FR subs (Crunchyroll)
- **Dataset size:** 38338 lines
- **Optimal hyperparameters:**
  - `alpha`: 1e-4
  - `power_syntactic`: 2
  - `power_positional`: 4
- **Performances:**
  - Top-1 accuracy: 70.9%
  - Top-3 accuracy: 93.3%


## TODO

- implement `process_subs_w_splitter`
- rebuild split dataset with subtitles durations
- find optimal ratios on the built dataset
- run tests