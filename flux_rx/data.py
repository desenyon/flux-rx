import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import yfinance as yf

from flux_rx.exceptions import FluxDataError
from flux_rx.logger import get_logger

_CACHE_DIR = Path.home() / ".flux_rx_cache"
_CACHE_EXPIRY_HOURS = 4

logger = get_logger(__name__)

PERIOD_MAP = {
    "1d": 1,
    "5d": 5,
    "1mo": 30,
    "3mo": 90,
    "6mo": 180,
    "1y": 365,
    "2y": 730,
    "5y": 1825,
    "10y": 3650,
    "ytd": None,
    "max": None,
}


def _ensure_cache_dir() -> Path:
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return _CACHE_DIR


def _cache_key(ticker: str, period: str, interval: str) -> str:
    raw = f"{ticker.upper()}_{period}_{interval}"
    return hashlib.md5(raw.encode()).hexdigest()


def _cache_path(key: str, suffix: str = ".parquet") -> Path:
    return _ensure_cache_dir() / f"{key}{suffix}"


def _is_cache_valid(path: Path, max_age_hours: float = _CACHE_EXPIRY_HOURS) -> bool:
    if not path.exists():
        return False
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    return datetime.now() - mtime < timedelta(hours=max_age_hours)


def clear_cache() -> int:
    cache_dir = _ensure_cache_dir()
    count = 0
    for f in cache_dir.glob("*"):
        try:
            f.unlink()
            count += 1
        except Exception as e:
            logger.warning(f"Failed to delete {f}: {e}")
    logger.info(f"Cleared {count} files from cache.")
    return count


def fetch(
    ticker: str,
    period: str = "5y",
    interval: str = "1d",
    use_cache: bool = True,
) -> pd.DataFrame:
    ticker = ticker.upper()
    key = _cache_key(ticker, period, interval)
    cache_file = _cache_path(key)

    if use_cache and _is_cache_valid(cache_file):
        try:
            df = pd.read_parquet(cache_file)
            df.index = pd.to_datetime(df.index)
            logger.info(f"Loaded {ticker} from cache.")
            return df
        except Exception as e:
            logger.warning(f"Failed to read cache for {ticker}: {e}")

    logger.info(f"Fetching {ticker} from Yahoo Finance (period={period}, interval={interval})...")
    try:
        yf_ticker = yf.Ticker(ticker)
        df = yf_ticker.history(period=period, interval=interval, auto_adjust=True)
    except Exception as e:
        logger.error(f"Error fetching {ticker}: {e}")
        raise FluxDataError(f"Failed to fetch {ticker}: {e}") from e

    if df.empty:
        logger.error(f"No data returned for {ticker}.")
        raise FluxDataError(f"No data found for ticker: {ticker}")

    df.index = pd.to_datetime(df.index)
    df.index.name = "Date"
    df = df[["Open", "High", "Low", "Close", "Volume"]]

    if use_cache:
        try:
            df.to_parquet(cache_file)
        except Exception as e:
            logger.warning(f"Failed to write cache for {ticker}: {e}")

    return df


def fetch_multiple(
    tickers: list[str],
    period: str = "5y",
    interval: str = "1d",
    use_cache: bool = True,
    max_workers: int = 10,
) -> dict[str, pd.DataFrame]:
    """Fetch multiple tickers concurrently."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {t: executor.submit(fetch, t, period, interval, use_cache) for t in tickers}
        return {t: f.result() for t, f in futures.items()}


def get_info(ticker: str, use_cache: bool = True) -> dict:
    ticker = ticker.upper()
    key = f"info_{ticker}"
    cache_file = _cache_path(key, suffix=".json")

    if use_cache and _is_cache_valid(cache_file, max_age_hours=24):
        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read info cache for {ticker}: {e}")

    logger.info(f"Fetching info for {ticker}...")
    try:
        yf_ticker = yf.Ticker(ticker)
        info = yf_ticker.info
    except Exception as e:
        logger.error(f"Error fetching info for {ticker}: {e}")
        raise FluxDataError(f"Failed to fetch info for {ticker}: {e}") from e

    clean_info = {
        "ticker": ticker,
        "name": info.get("longName") or info.get("shortName") or ticker,
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "country": info.get("country", "N/A"),
        "market_cap": info.get("marketCap"),
        "market_cap_fmt": _format_market_cap(info.get("marketCap")),
        "currency": info.get("currency", "USD"),
        "exchange": info.get("exchange", "N/A"),
        "quote_type": info.get("quoteType", "EQUITY"),
        "description": info.get("longBusinessSummary", ""),
        "website": info.get("website", ""),
        "employees": info.get("fullTimeEmployees"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "dividend_yield": info.get("dividendYield"),
        "beta": info.get("beta"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "avg_volume": info.get("averageVolume"),
        "avg_volume_10d": info.get("averageDailyVolume10Day"),
    }

    if use_cache:
        try:
            with open(cache_file, "w") as f:
                json.dump(clean_info, f, indent=2, default=str)
        except Exception as e:
            logger.warning(f"Failed to write info cache for {ticker}: {e}")

    return clean_info


def _format_market_cap(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    if value >= 1e12:
        return f"${value / 1e12:.2f}T"
    if value >= 1e9:
        return f"${value / 1e9:.2f}B"
    if value >= 1e6:
        return f"${value / 1e6:.2f}M"
    return f"${value:,.0f}"


def get_benchmark_data(
    benchmark: str = "SPY",
    period: str = "5y",
    interval: str = "1d",
) -> pd.DataFrame:
    return fetch(benchmark, period, interval)


def align_dataframes(
    dfs: dict[str, pd.DataFrame],
    column: str = "Close",
) -> pd.DataFrame:
    aligned = pd.DataFrame()
    for ticker, df in dfs.items():
        aligned[ticker] = df[column]
    aligned = aligned.dropna()
    return aligned


def normalize_prices(df: pd.DataFrame, base: float = 100.0) -> pd.DataFrame:
    return df / df.iloc[0] * base
