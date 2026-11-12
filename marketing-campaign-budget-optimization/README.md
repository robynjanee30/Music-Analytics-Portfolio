# Marketing Campaign Performance & Budget Optimization

Robyn Moore · Analytics portfolio · Excel and Tableau

**Where should the next advertising dollar go?** I analyzed 190 ad-group-month observations from July through November 2021, rebuilt the campaign KPIs, and modeled a $10,000 test budget.

[Read the case study](case-study.pdf) · [Recalculate the KPIs](verify_metrics.py) · [Portfolio home](../)

## What I found

| Measure | July–November 2021 |
| --- | ---: |
| Ad spend | $635,372 |
| Tracked revenue | $561,960 |
| Revenue less ad spend | −$73,412 |
| ROAS | 0.88× |
| Media ROI | −11.55% |

- **Conversion volume was a poor proxy for return.** November drove 43,267 conversions and returned 0.90× on ad spend. October was the only month above 1.00×.
- **Promo Code led the recurring themes at 0.93× ROAS.** Sale returned 0.40×. Black Friday/Cyber Monday returned 4.36× across two records and $47 of spend, so I treated it as a seasonal retest.
- **The proposed mix still needs improvement.** Allocate $4,000 to Promo Code, $3,000 to Promo, $2,000 to Coupon Code and retain $1,000. Applying historical ROAS to the $9,000 deployed gives $8,267.03 in modeled revenue. Covering media spend requires $732.97 more, an 8.87% lift over modeled revenue.

## Tableau dashboard

![Executive Tableau dashboard showing overall KPIs, monthly conversions, spend, revenue and ROI](tableau-overview.jpg)

The original Tableau labels “P&L” and “profitable” refer to tracked revenue less ad spend and media break-even. They exclude product margins and other operating costs.

[Campaign strategy view](tableau-campaign-strategy.jpg) · [Budget optimization view](tableau-budget-optimization.jpg)

## Excel decision support

[Campaign decision tool](excel-decision-tool.jpg) · [Budget reallocation scenario](excel-budget-scenario.jpg)

The decision tool retrieves weighted KPIs for a selected promotion and recommends an action based on performance and scale. The scenario applies historical theme ROAS to an editable allocation. The links above are screenshots from the original Tableau and Excel work.

## Data and methods

Source: [Shopping Mall Paid Search Campaign Dataset on Kaggle](https://www.kaggle.com/datasets/marceaxl82/shopping-mall-paid-search-campaign-dataset/data). To reproduce the headline tables and scenario, download the source CSV and run `python3 verify_metrics.py path/to/source.csv` with Python 3.10 or later.

I recalculated the inconsistent source conversion rate from conversions and clicks and used ratios of sums for all aggregate efficiency metrics. Media ROI measures revenue less ad spend divided by ad spend. It excludes margin and other operating costs. The allocation is a historical scenario. Future budgets should be evaluated using controlled tests and incremental return.
