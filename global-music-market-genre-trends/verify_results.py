"""Verify Project 4 from the exported aggregate tables. Requires pandas and scikit-learn."""
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent


def shares(data, keys):
    totals = data.groupby([*keys, "genre_family"])["streams"].sum().unstack(fill_value=0)
    return totals.div(totals.sum(axis=1), axis=0)


def require_equal(actual, expected):
    aligned = actual.reindex(index=expected.index, columns=expected.columns)
    np.testing.assert_allclose(aligned, expected, rtol=1e-8, atol=1e-10)


def main():
    with ZipFile(ROOT / "aggregate-results.zip") as archive:
        def read(prefix):
            name, = [name for name in archive.namelist() if name.startswith(prefix + "_")]
            with archive.open(name) as source:
                return pd.read_csv(source)

        quality = read("01")
        assert quality["raw_rows"].sum() == 21_257_472
        assert quality["rows_removed"].sum() == 2_000
        assert quality["unmatched_song_rows"].sum() == 0

        data = read("02")
        data = data.loc[data["market"].ne("global") & ~data["genre_family"].isin(["Other", "Unknown"])].copy()
        data["year"] = pd.to_datetime(data["month"]).dt.year
        yearly = data[data["year"].between(2018, 2021)]
        current = yearly[yearly["year"].eq(2021)]
        coverage = current.groupby("market")["month"].nunique()
        profile = shares(current[current["market"].isin(coverage[coverage.eq(12)].index)], ["market"])
        assert len(profile) == 65

        reference = read("03")
        require_equal(profile, reference.pivot(index="market", columns="genre_family", values="genre_share"))
        affinity = profile.div(profile.mean())
        require_equal(affinity, reference.pivot(index="market", columns="genre_family", values="over_index"))
        reach = read("07").set_index("genre_family")
        pd.testing.assert_series_equal(profile.ge(0.05).sum().reindex(reach.index), reach["markets_above_5pct"], check_names=False)

        coverage = yearly.groupby("market")["month"].nunique()
        balanced = coverage[coverage.eq(48)].index
        assert len(balanced) == 52
        annual = shares(yearly[yearly["market"].isin(balanced)], ["year", "market"])
        trend = annual.groupby("year").mean().mul(100).T
        trend.columns = trend.columns.astype(str)
        require_equal(trend, read("05").set_index("genre_family")[["2018", "2019", "2020", "2021"]])
        opportunities = read("06").set_index(["market", "genre_family"])
        change = (annual.loc[2021] - annual.loc[2018]).mul(100).stack()
        np.testing.assert_allclose(change.reindex(opportunities.index), opportunities["change_pp"], atol=1e-9)

        clusters = read("08").set_index("market")
        inputs = profile.loc[clusters.index, clusters.columns.drop("cluster")]
        scores = {}
        for k in range(2, 9):
            labels = KMeans(n_clusters=k, n_init=20, random_state=42).fit_predict(inputs)
            scores[k] = silhouette_score(inputs, labels)
            if k == 5:
                agreement = adjusted_rand_score(clusters["cluster"], labels)
        assert agreement == 1
        assert round(scores[2], 3) == 0.530 and round(scores[5], 3) == 0.521

        similarity = pd.Series(cosine_similarity(profile, profile.loc[["gb"]]).ravel(), index=profile.index)
        for prefix, genre in [("09", "Rock / Alternative"), ("10", "Electronic / Dance")]:
            reference = read(prefix).set_index("market")
            measured = pd.DataFrame({
                "similarity": similarity,
                "genre_share_pct": profile[genre].mul(100),
                "over_index": affinity[genre],
            }).reindex(reference.index).round(3)
            require_equal(measured, reference)

    print("Verified: 65 current markets, 52 balanced trend markets, genre shares, affinity, reach, growth and UK shortlist values.")
    print(f"Silhouette: k=2 {scores[2]:.3f}, k=5 {scores[5]:.3f}. Exported cluster assignment agreement: {agreement:.0%}.")


if __name__ == "__main__":
    main()
