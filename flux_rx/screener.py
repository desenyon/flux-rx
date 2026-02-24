# Flux-RX Screener Module: Stock ranking and filtering
from __future__ import annotations

import pandas as pd
from typing import List, Optional
from flux_rx.data import fetch_multiple
from flux_rx.analytics import compute_metrics


def screen_tickers(
    tickers: List[str], period: str = "1y", sort_by: str = "sharpe_ratio", ascending: bool = False
) -> pd.DataFrame:
    """
    Fetch and rank multiple tickers based on performance metrics.
    """
    data = fetch_multiple(tickers, period=period)
    results = []

    for ticker, df in data.items():
        try:
            metrics = compute_metrics(df["Close"])
            metrics["ticker"] = ticker
            results.append(metrics)
        except Exception:
            continue

    screen_df = pd.DataFrame(results)
    if not screen_df.empty:
        screen_df = screen_df.set_index("ticker").sort_values(sort_by, ascending=ascending)

    return screen_df
