"""Recalculate campaign KPIs from the supplied Kaggle CSV. Python 3.10+."""
import argparse
import csv
from collections import defaultdict
from fractions import Fraction
from statistics import correlation

MONTHS = ("July", "August", "September", "October", "November")
SHOP_THEMES = {
    "[shop coupon code]": "Coupon Code",
    "[shop coupon]": "Coupon",
    "[shop discount code]": "Discount Code",
    "[shop promo code]": "Promo Code",
    "[shop promo]": "Promo",
}
FIELDS = ("Impressions", "Clicks", "Conversions", "Cost", "Revenue")
ALLOCATION = {"Promo Code": 4_000, "Promo": 3_000, "Coupon Code": 2_000}
TEST_BUDGET = 10_000


def ratio(numerator, denominator):
    return Fraction(numerator, denominator) if denominator else None


def aggregate(rows):
    m = {field: sum(int(row[field]) for row in rows) for field in FIELDS}
    impressions, clicks, conversions, cost, revenue = (m[k] for k in FIELDS)
    return {
        **m, "Records": len(rows), "Revenue less ad spend": revenue - cost,
        "CTR": ratio(clicks, impressions), "CVR": ratio(conversions, clicks),
        "CPC": ratio(cost, clicks), "CPA": ratio(cost, conversions),
        "ROAS": ratio(revenue, cost), "Media ROI": ratio(revenue - cost, cost),
    }


def summarize(rows):
    months = defaultdict(list)
    themes = defaultdict(list)
    for row in rows:
        months[row["Month"]].append(row)
        suffix = row["Ad Group"].split(" - ", 3)[-1].strip()
        themes[SHOP_THEMES.get(suffix, suffix)].append(row)

    monthly = {month: aggregate(months[month]) for month in MONTHS}
    promotion = {theme: aggregate(group) for theme, group in sorted(themes.items())}
    deployed = sum(ALLOCATION.values())
    revenue = sum(amount * promotion[theme]["ROAS"] for theme, amount in ALLOCATION.items())
    scenario = {
        "Deployed": deployed, "Reserve": TEST_BUDGET - deployed,
        "Scenario revenue": revenue, "Scenario ROAS": revenue / deployed,
        "Break-even gap": deployed - revenue, "Required revenue lift": (deployed - revenue) / revenue,
    }
    return aggregate(rows), monthly, promotion, scenario


def show_kpis(label, kpis):
    print(f"{label:28} {kpis['Records']:3} rows | "
          f"${kpis['Cost']:>7,} spend | ${kpis['Revenue']:>7,} revenue | "
          f"{float(kpis['ROAS']):.4f}x ROAS | {float(kpis['Media ROI']):+.2%} media ROI")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=argparse.FileType("r", encoding="utf-8-sig"))
    args = parser.parse_args()
    with args.csv_file as source:
        rows = list(csv.DictReader(source))
    overall, monthly, promotion, scenario = summarize(rows)
    for label, kpis in [("Overall", overall), *monthly.items(), *promotion.items()]:
        show_kpis(label, kpis)

    paid = [(int(r["Cost"]), int(r["Revenue"])) for r in rows if int(r["Cost"]) > 0]
    costs, revenues = zip(*paid)
    print(f"Row-level cost vs revenue r = {correlation(costs, revenues):.4f}")
    print(f"Row-level cost vs ROAS r = {correlation(costs, [r/c for c, r in paid]):.4f}")
    for key, value in scenario.items():
        print(f"{key}: {float(value):.6g}")


if __name__ == "__main__":
    main()
