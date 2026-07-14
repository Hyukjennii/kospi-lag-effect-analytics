"""
test_stationarity.py

Runs ADF and KPSS stationarity tests on kospi_close, base_rate, usd_krw.
A series that is non-stationary (ADF fails to reject unit root, KPSS rejects
stationarity) should be differenced before use in OLS/VAR to avoid spurious
regression.

Output: results/stationarity_results.csv
"""

import pandas as pd
# TODO: from statsmodels.tsa.stattools import adfuller, kpss

SERIES_TO_TEST = ["kospi_close", "base_rate", "usd_krw"]


def run_adf(series: pd.Series) -> dict:
    """Run Augmented Dickey-Fuller test. Returns {statistic, p_value, is_stationary}."""
    # TODO: result = adfuller(series.dropna())
    # ADF null hypothesis = unit root (non-stationary). Reject if p < 0.05.
    raise NotImplementedError


def run_kpss(series: pd.Series) -> dict:
    """Run KPSS test. Returns {statistic, p_value, is_stationary}.
    Note: KPSS null hypothesis = stationary (opposite of ADF) — use both together.
    """
    # TODO: result = kpss(series.dropna(), regression='c')
    raise NotImplementedError


def run_all(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in SERIES_TO_TEST:
        adf_result = run_adf(df[col])
        kpss_result = run_kpss(df[col])
        rows.append({"series": col, **adf_result, **kpss_result})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = pd.read_csv("data/merged_raw.csv", parse_dates=["date"])
    results = run_all(df)
    results.to_csv("results/stationarity_results.csv", index=False)
    print(results)
