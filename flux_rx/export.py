# Flux-RX Export Module: Saving data and metrics
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional, Union

import pandas as pd
from flux_rx.analytics import compute_metrics
from flux_rx.data import fetch


def export(
    ticker: str,
    format: str = "csv",
    path: Optional[Union[str, Path]] = None,
    period: str = "5y",
    include_metrics: bool = True,
) -> str:
    """Export ticker data and optionally metrics to a file."""
    format = format.lower()
    df = fetch(ticker, period=period)
    
    if path is None:
        path = f"{ticker.lower()}_export.{format}"
    
    path = Path(path)
    
    if format == "csv":
        df.to_csv(path)
    elif format == "json":
        if include_metrics:
            data = {
                "ticker": ticker,
                "data": df.to_dict(orient="index"),
                "metrics": compute_metrics(df["Close"])
            }
            with open(path, "w") as f:
                json.dump(data, f, indent=4, default=str)
        else:
            df.to_json(path, orient="index", date_format="iso")
    elif format == "excel" or format == "xlsx":
        try:
            import openpyxl  # Check if installed
        except ImportError:
            raise ImportError("Exporting to Excel requires 'openpyxl'. Install it with 'pip install openpyxl'.")
            
        with pd.ExcelWriter(path) as writer:
            df.to_excel(writer, sheet_name="Data")
            if include_metrics:
                m = compute_metrics(df["Close"])
                m_df = pd.DataFrame(list(m.items()), columns=["Metric", "Value"])
                m_df.to_excel(writer, sheet_name="Metrics", index=False)
    else:
        raise ValueError(f"Unsupported export format: {format}")
        
    return str(path.absolute())
