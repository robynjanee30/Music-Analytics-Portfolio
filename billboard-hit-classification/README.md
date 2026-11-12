# Can audio features identify Billboard hits?

Robyn Moore · Music analytics portfolio · Python, pandas, scikit-learn

**Can a small set of musical descriptors distinguish songs with a recorded Billboard Hot 100 appearance?** I tested 12 audio features on a historical benchmark and used a release-year split to separate training, model selection, and evaluation.

[Read the case study](case-study.pdf) · [View the notebook](billboard-hit-classification.ipynb) · [Portfolio home](../)

## What I found

| Test metric | Random Forest | Always non-hit |
| --- | ---: | ---: |
| ROC-AUC | 0.678 | 0.500 |
| Balanced accuracy | 63.6% | 50.0% |
| Accuracy | 61.3% | 67.2% |
| Hit recall | 70.3% | 0.0% |
| Hit precision | 44.3% | Undefined |

The forest found **557 of 792 labelled hits** and flagged **699 non-hits**. Audio descriptors provided a modest historical ranking signal, with enough false positives to make an automatic shortlist impractical on its own.

## How I tested it

- Joined the HSP-S audio and release-year files by UUID. Of 7,736 audio records, 7,281 entered the model after filtering to known release years from 1960 to 2009.
- Trained on **1960–1989** (2,907 songs), selected the model and threshold on **1990–1999** (1,961), and held out **2000–2009** (2,413).
- Compared a training-majority dummy, Logistic Regression and Random Forest by validation ROC-AUC. Selected the forest by validation ROC-AUC and a **0.65** cutoff by validation balanced accuracy, then applied both to the test set.
- Used only audio predictors. Artist information was used to audit overlap: 236 test songs featured a training-period artist.

The benchmark deliberately samples hits and non-hits. Its chart labels are retrospective, and the release-year split does not guarantee that labels were known at each cutoff. The findings describe historical classification. A commercial forecast would need pre-release inputs, a fixed outcome window and a separate evaluation.

## Run the notebook

Use Python 3.12. Download `hsp-s_acousticbrainz.parquet` and `hsp-s_uuid_year.csv` from [the HSP-S Zenodo release](https://zenodo.org/records/5383858), place both beside the notebook, and run `python -m pip install -r requirements.txt`. Then start JupyterLab and run all cells. The notebook includes saved aggregate metrics and plots for browser review.

Data and paper: Michael Vötter, Maximilian Mayerl, Günther Specht and Eva Zangerle (2021), [Novel Datasets for Evaluating Song Popularity Prediction Tasks](https://doi.org/10.1109/ISM52913.2021.00034).
