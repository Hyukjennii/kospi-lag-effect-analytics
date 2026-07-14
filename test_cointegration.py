"""
test_cointegration.py

Tests whether kospi_close, base_rate, usd_krw share a genuine long-run
equilibrium relationship (cointegration), as opposed to a spurious one.

- Engle-Granger: pairwise (e.g. kospi vs rate, kospi vs fx)
- Johansen: multivariate (all three series jointly)

Output: results/cointegration_results.csv
"""

import pandas as pd
# TODO: from statsmodels.tsa.stattools import coint
# TODO: from statsmodels.tsa.vector_ar.vecm import coint_johansen


def run_engle_granger(series_a: pd.Series, series_b: pd.Series) -> dict:
    """Pairwise Engle-Granger cointegration test."""
    # TODO: score, p_value, _ = coint(series_a.dropna(), series_b.dropna())
    raise NotImplementedError


def run_johansen(df: pd.DataFrame, det_order: int = 0, k_ar_diff: int = 1) -> dict:
    """Multivariate Johansen cointegration test on [kospi_close, base_rate, usd_krw]."""
    # TODO: result = coint_johansen(df[["kospi_close", "base_rate", "usd_krw"]], det_order, k_ar_diff)
    raise NotImplementedError


if __name__ == "__main__":
    df = pd.read_csv("data/merged_raw.csv", parse_dates=["date"])
    eg_rate = run_engle_granger(df["kospi_close"], df["base_rate"])
    eg_fx = run_engle_granger(df["kospi_close"], df["usd_krw"])
    johansen = run_johansen(df)
    # TODO: save all results to results/cointegration_results.csv
    print(eg_rate, eg_fx, johansen)
