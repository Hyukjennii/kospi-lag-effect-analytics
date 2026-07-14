"""
collect_data.py

Collects and merges the three core series for this project:
- KOSPI OHLCV (FinanceDataReader)
- Base rate (Bank of Korea ECOS API)
- USD/KRW exchange rate (Bank of Korea ECOS API)

Output: data/merged_raw.csv with columns [date, kospi_close, kospi_volume, base_rate, usd_krw]
"""

import pandas as pd

# TODO: import FinanceDataReader as fdr
# TODO: set ECOS_API_KEY via environment variable, never hardcode it

START_DATE = "2010-01-01"
END_DATE = None  # None = today


def fetch_kospi(start: str, end: str | None) -> pd.DataFrame:
    """Fetch KOSPI OHLCV data. Returns DataFrame indexed by date."""
    # TODO: df = fdr.DataReader('KS11', start, end)
    raise NotImplementedError


def fetch_base_rate(start: str, end: str | None) -> pd.DataFrame:
    """Fetch base rate from ECOS API. Returns DataFrame indexed by date."""
    # TODO: call ECOS API, statistic code for base rate
    raise NotImplementedError


def fetch_usd_krw(start: str, end: str | None) -> pd.DataFrame:
    """Fetch USD/KRW exchange rate from ECOS API. Returns DataFrame indexed by date."""
    # TODO: call ECOS API, statistic code for USD/KRW
    raise NotImplementedError


def merge_and_save(output_path: str = "data/merged_raw.csv") -> pd.DataFrame:
    """Merge all sources on date and save to CSV."""
    kospi = fetch_kospi(START_DATE, END_DATE)
    rate = fetch_base_rate(START_DATE, END_DATE)
    fx = fetch_usd_krw(START_DATE, END_DATE)

    merged = kospi.join(rate, how="left").join(fx, how="left")
    # TODO: decide on forward-fill policy for lower-frequency series (rate is monthly, KOSPI is daily)
    merged.to_csv(output_path)
    return merged


if __name__ == "__main__":
    merge_and_save()
