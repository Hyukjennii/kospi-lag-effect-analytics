"""
train_baselines.py

Trains classical time-series baselines: ARIMA, VAR, and the original
lag-effect linear regression. These exist so the ML models in
train_models.py have something honest to be compared against.

Output: models/baseline_*.pkl, results/baseline_predictions.csv
"""

import pandas as pd
# TODO: from statsmodels.tsa.arima.model import ARIMA
# TODO: from statsmodels.tsa.vector_ar.var_model import VAR
# TODO: import statsmodels.api as sm  (for the lag regression)


def train_arima(train_series: pd.Series, order: tuple[int, int, int] = (1, 1, 1)):
    raise NotImplementedError


def train_var(train_df: pd.DataFrame, maxlags: int = 5):
    raise NotImplementedError


def train_lag_regression(train_df: pd.DataFrame):
    """KOSPI ~ base_rate_lag + usd_krw_lag, OLS."""
    raise NotImplementedError


if __name__ == "__main__":
    df = pd.read_csv("data/features.csv", parse_dates=["date"])
    # TODO: chronological train/val/test split - see build_features.py note on no shuffling
