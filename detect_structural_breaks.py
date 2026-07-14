"""
detect_structural_breaks.py

Detects whether the KOSPI ~ base_rate + usd_krw relationship is stable over
time, using:
- Chow test at candidate break dates (e.g. COVID-19 onset, rate-hike cycle starts)
- CUSUM test for detecting breaks without pre-specifying a date

Output: results/structural_break_results.csv + docs/diagrams/cusum_plot.png
"""

import pandas as pd
# TODO: consider the `ruptures` package for CUSUM-style change point detection

CANDIDATE_BREAK_DATES = [
    "2020-02-01",  # COVID-19 onset
    # TODO: add major rate-hike cycle start dates
]


def run_chow_test(df: pd.DataFrame, break_date: str) -> dict:
    """Chow test: compares a single regression on the full sample against
    two separate regressions split at break_date. Large F-stat / low p-value
    suggests a structural break at that point."""
    raise NotImplementedError


def run_cusum(df: pd.DataFrame) -> dict:
    """CUSUM-based break detection without a pre-specified date."""
    # TODO: use ruptures.Pelt or similar on the regression residuals
    raise NotImplementedError


if __name__ == "__main__":
    df = pd.read_csv("data/merged_raw.csv", parse_dates=["date"])
    chow_results = [run_chow_test(df, d) for d in CANDIDATE_BREAK_DATES]
    cusum_result = run_cusum(df)
    print(chow_results, cusum_result)
