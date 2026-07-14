"""
build_features.py

Builds engineered features for the ML models. CRITICAL: every feature for
date t must use only data available up to and including date t — never future
data. See tests/test_no_leakage.py for the checks this must satisfy.

Output: data/features.csv
"""

import pandas as pd


def add_lag_features(df: pd.DataFrame, cols: list[str], lags: list[int]) -> pd.DataFrame:
    for col in cols:
        for lag in lags:
            df[f"{col}_lag{lag}"] = df[col].shift(lag)  # shift() looks backward only - safe
    return df


def add_moving_averages(df: pd.DataFrame, col: str, windows: list[int]) -> pd.DataFrame:
    for w in windows:
        # .rolling(w).mean() at row t uses rows [t-w+1, t] only - safe, no leakage
        df[f"{col}_ma{w}"] = df[col].rolling(w).mean()
    return df


def add_volatility(df: pd.DataFrame, col: str, window: int = 20) -> pd.DataFrame:
    df[f"{col}_vol{window}"] = df[col].pct_change().rolling(window).std()
    return df


def add_rsi(df: pd.DataFrame, col: str, window: int = 14) -> pd.DataFrame:
    # TODO: implement RSI using only past `window` days at each point
    raise NotImplementedError


def build_all_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_lag_features(df, ["base_rate", "usd_krw"], lags=[1, 2, 3])
    df = add_moving_averages(df, "kospi_close", windows=[5, 20, 60])
    df = add_volatility(df, "kospi_close")
    df = add_rsi(df, "kospi_close")
    return df.dropna()  # drop rows with NaN from lag/rolling warmup


if __name__ == "__main__":
    df = pd.read_csv("data/merged_raw.csv", parse_dates=["date"])
    features = build_all_features(df)
    features.to_csv("data/features.csv", index=False)
