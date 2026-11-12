# Audience Segmentation & Fan Strategy

Robyn Moore · Music analytics portfolio · Python, pandas, scikit-learn

**How can a label use listening behavior to decide who might respond to artist discovery or catalog re-engagement?** I used historical Last.fm listening histories to identify two behavioral segments, then compared artist reach and audience affinity to design campaign tests.

[Read the case study](case-study.pdf) · [View the Python notebook](audience-segmentation.ipynb) · [Portfolio home](../)

## What I found

The original full-cohort analysis parsed **19,098,853 events across 992 users**. The 500-play minimum retained **926 listeners**.

| Historical cohort average | Focused Listeners | Exploratory Power Listeners |
| --- | ---: | ---: |
| Listeners | 454 (49%) | 472 (51%) |
| Plays per observation day | 9.67 | 42.19 |
| Artist breadth per observation day | 0.62 | 2.49 |
| Share of plays for top artist | 8.67% | 5.92% |
| Active-day rate | 28.22% | 71.36% |

Artist breadth divides the number of distinct artist names across a listener’s history by their observation days. The Exploratory Power segment logged about 4.4× more plays per day and spread its listening more widely.

**Reach and affinity tell different stories.** Radiohead reached 693 listeners and indexed at 1.15×. Beach House reached 19.28% of Exploratory Power Listeners and 3.96% of Focused Listeners, an index of 4.86×. Flying Lotus indexed at 7.37×, with 14.62% penetration in the Exploratory Power segment.

![Artist reach by segment for Radiohead, Beach House, Flying Lotus and Modeselektor](artist-affinity.png)

Radiohead shows broad reach in both segments. Beach House, Flying Lotus and Modeselektor (3.5% of Focused and 17.4% of Exploratory Power Listeners) reach far fewer listeners overall and are concentrated in the higher-volume segment.

**Interpretation.** “Exploratory Power” is a label for the higher-volume cluster with wider daily artist breadth. It does not show a stronger appetite for discovery. Artist breadth was normalized by time. Plays and breadth increased by similar multiples across segments, so these averages do not establish greater exploration per play. A high-volume listener also has more chances to play any given artist at least once. The affinity ratios are descriptive. I’d compare listeners at similar play volumes or test breadth per play before interpreting them as preference differences.

## What I’d test

- **Discovery for Exploratory Power Listeners.** Test an adjacent-artist recommendation seeded by a high-affinity artist. Measure first-time artist listens and repeat listening against a holdout.
- **Catalog re-engagement for Focused Listeners.** Test a recommendation anchored in a familiar artist. Measure catalog plays and repeat engagement against a holdout.

## How the model was checked

I standardized four behavioral features and compared K-Means solutions from k=2 to k=8. The two-cluster solution led with a silhouette score of 0.3323. Raising the minimum history to 1,000 plays preserved 870 of 890 overlapping assignments (97.75%). The score supports directional profiles. The historical cohort and inconsistent artist metadata limit generalization to current audiences.

## Run the analysis

1. Download the full `userid-timestamp-artid-artname-traid-traname.tsv.zip` from the [Last.fm 1K data release](https://github.com/eifuentes/lastfm-dataset-1K/releases) and place it beside the notebook.
2. Install the dependencies with `python -m pip install -r requirements.txt`, then open `audience-segmentation.ipynb` in JupyterLab and run all cells. The code reads the event archive in chunks.
3. The notebook is published without saved cell outputs and records the original aggregate results as notes under each step. The full archive is required to reproduce the historical figures. A 50-user Parquet subset from the same release was used for exploration only. Raw histories and demographics are omitted from this repository.

Source: Òscar Celma’s Last.fm 1K user dataset, released via the mirror linked above.
