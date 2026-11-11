# Where streaming growth comes from

Robyn Moore · Music analytics portfolio · Spotify Charts, 2017–2021

A fictional record label wants to know which markets deserve a closer look and what drives an artist’s streaming gains. I used PostgreSQL and DBeaver to analyze historical Spotify Charts records and Power BI to build a dashboard.

## What I found

- **Scale.** Ed Sheeran led artist credits with 10.52B recorded chart streams. The Weeknd’s “Blinding Lights” led tracks at 2.56B. The United States led markets at 142.13B.
- **Geography.** Mata and sanah each over-indexed 56.9× in Poland in 2021. The index compares the artist’s share of streams from Poland with Poland’s share of all included chart streams. I paired the index with volume thresholds to surface markets worth researching for local promotion.
- **Momentum.** João Gomes gained 414.1M recorded chart streams from H1 to H2 2021, with 60% of H2 volume across his two leading tracks. Baby Keem gained 129.0M, with 81% of H2 volume from “family ties.” I’d test a multi-track campaign for João Gomes and use Baby Keem’s breakout to introduce listeners to the rest of his catalog.

## Project files

| Path | Contents |
| --- | --- |
| `sql/analysis.sql` | Eight read-only PostgreSQL queries for the rankings, over-index and momentum analysis |
| `data/` | Eight aggregated exports used to check the case-study figures |

The SQL expects a prepared PostgreSQL table named `charts` scoped to 2017–2021. Required fields are `date` (date or timestamp), `artist`, `title` and `region` (text), and `streams` (numeric, nullable). Run the statements in order or individually. Each query is labeled with its corresponding export. The raw input and its original download URL were not included in the materials available for this release, so a full rebuild from raw records requires the original source.

## Method notes

The analysis excludes missing stream counts and the aggregate Global chart. The 2021 comparisons also exclude South Korea because its chart series began partway through the year. Artist credits stay as written, so collaborative credits are grouped separately. The two case-study track queries consolidate title capitalization variants.

Market over-index uses the artist’s share of streams from a market divided by the market’s share of all included streams. The screen requires 100M streams for the artist credit and 10M for the artist-market pair. The momentum sample requires at least 1M H1 streams, 10M H2 streams and a gain of 100M, then keeps up to 20 credits ranked by percentage growth.

Chart streams capture charting activity. Market coverage changed over time, and these historical results do not establish what caused the growth.
