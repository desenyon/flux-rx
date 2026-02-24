# Flux-RX Analytics Module: Financial metrics and calculations
from __future__ import annotations

from typing import Optional, Union

import numpy as np
import pandas as pd

from flux_rx.exceptions import FluxComputeError
from flux_rx.logger import get_logger

logger = get_logger(__name__)

TRADING_DAYS_PER_YEAR = 252
_RISK_FREE_RATE = 0.04


def _validate_prices(prices: pd.Series, name: str = "prices") -> None:
    if prices is None or prices.empty:
        logger.error(f"Cannot compute metrics on empty series: {name}")
        raise FluxComputeError(f"Input series '{name}' is empty.")
    if len(prices) < 2:
        logger.error(f"Not enough data points in {name} to compute returns.")
        raise FluxComputeError(f"Input series '{name}' must have at least 2 data points.")


def set_risk_free_rate(rate: float) -> None:
    """Set the global risk-free rate."""
    global _RISK_FREE_RATE
    _RISK_FREE_RATE = rate


def get_risk_free_rate() -> float:
    """Get the global risk-free rate."""
    return _RISK_FREE_RATE


def daily_returns(prices: pd.Series) -> pd.Series:
    _validate_prices(prices)
    return prices.pct_change().dropna()


def cumulative_returns(prices: pd.Series) -> pd.Series:
    returns = daily_returns(prices)
    return (1 + returns).cumprod() - 1


def total_return(prices: pd.Series) -> float:
    return (prices.iloc[-1] / prices.iloc[0]) - 1


def cagr(prices: pd.Series) -> float:
    _validate_prices(prices)
    total_days = (prices.index[-1] - prices.index[0]).days
    if total_days <= 0:
        return 0.0
    years = total_days / 365.25
    total_ret = total_return(prices)
    try:
        return (1 + total_ret) ** (1 / years) - 1
    except Exception as e:
        logger.error(f"Error calculating CAGR: {e}")
        raise FluxComputeError(f"Error calculating CAGR: {e}") from e


def volatility(prices: pd.Series, annualize: bool = True) -> float:
    returns = daily_returns(prices)
    vol = returns.std()
    if annualize:
        vol *= np.sqrt(TRADING_DAYS_PER_YEAR)
    return vol


def max_drawdown(prices: pd.Series) -> float:
    cummax = prices.cummax()
    drawdown = (prices - cummax) / cummax
    return drawdown.min()


def drawdown_series(prices: pd.Series) -> pd.Series:
    cummax = prices.cummax()
    return (prices - cummax) / cummax


def sharpe_ratio(
    prices: pd.Series,
    risk_free_rate: Optional[float] = None,
) -> float:
    if risk_free_rate is None:
        risk_free_rate = _RISK_FREE_RATE
    returns = daily_returns(prices)
    excess_returns = returns - risk_free_rate / TRADING_DAYS_PER_YEAR
    if returns.std() == 0:
        return 0.0
    return (excess_returns.mean() / returns.std()) * np.sqrt(TRADING_DAYS_PER_YEAR)


def sortino_ratio(
    prices: pd.Series,
    risk_free_rate: Optional[float] = None,
) -> float:
    if risk_free_rate is None:
        risk_free_rate = _RISK_FREE_RATE
    returns = daily_returns(prices)
    excess_returns = returns - risk_free_rate / TRADING_DAYS_PER_YEAR
    downside_returns = returns[returns < 0]
    if len(downside_returns) == 0 or downside_returns.std() == 0:
        return 0.0
    return (excess_returns.mean() / downside_returns.std()) * np.sqrt(TRADING_DAYS_PER_YEAR)


def calmar_ratio(prices: pd.Series) -> float:
    ann_return = cagr(prices)
    mdd = abs(max_drawdown(prices))
    if mdd == 0:
        return 0.0
    return ann_return / mdd


def rolling_volatility(
    prices: pd.Series,
    window: int = 21,
    annualize: bool = True,
) -> pd.Series:
    returns = daily_returns(prices)
    roll_vol = returns.rolling(window=window).std()
    if annualize:
        roll_vol *= np.sqrt(TRADING_DAYS_PER_YEAR)
    return roll_vol


def rolling_sharpe(
    prices: pd.Series,
    window: int = 63,
    risk_free_rate: Optional[float] = None,
) -> pd.Series:
    if risk_free_rate is None:
        risk_free_rate = _RISK_FREE_RATE
    returns = daily_returns(prices)
    excess_returns = returns - risk_free_rate / TRADING_DAYS_PER_YEAR
    roll_mean = excess_returns.rolling(window=window).mean()
    roll_std = returns.rolling(window=window).std()
    return (roll_mean / roll_std) * np.sqrt(TRADING_DAYS_PER_YEAR)


def rolling_beta(
    prices: pd.Series,
    benchmark_prices: pd.Series,
    window: int = 63,
) -> pd.Series:
    returns = daily_returns(prices)
    bench_returns = daily_returns(benchmark_prices)
    aligned = pd.DataFrame({"asset": returns, "bench": bench_returns}).dropna()

    betas = []
    for i in range(len(aligned)):
        if i < window:
            betas.append(np.nan)
        else:
            w = aligned.iloc[i - window : i]
            cov = w["asset"].cov(w["bench"])
            var = w["bench"].var()
            betas.append(cov / var if var != 0 else np.nan)
    return pd.Series(betas, index=aligned.index)


def beta(prices: pd.Series, benchmark_prices: pd.Series) -> float:
    returns = daily_returns(prices)
    bench_returns = daily_returns(benchmark_prices)
    aligned = pd.DataFrame({"asset": returns, "bench": bench_returns}).dropna()
    cov_val = aligned["asset"].cov(aligned["bench"])
    var_val = aligned["bench"].var()
    cov: float = cov_val  # type: ignore[assignment]
    var: float = var_val  # type: ignore[assignment]
    return cov / var if var != 0 else 0.0


def alpha(
    prices: pd.Series,
    benchmark_prices: pd.Series,
    risk_free_rate: Optional[float] = None,
) -> float:
    if risk_free_rate is None:
        risk_free_rate = _RISK_FREE_RATE
    asset_return = cagr(prices)
    bench_return = cagr(benchmark_prices)
    b = beta(prices, benchmark_prices)
    return asset_return - (risk_free_rate + b * (bench_return - risk_free_rate))


def tracking_error(prices: pd.Series, benchmark_prices: pd.Series, annualize: bool = True) -> float:
    """Calculate the tracking error (standard deviation of active returns)."""
    returns = daily_returns(prices)
    bench_returns = daily_returns(benchmark_prices)
    aligned = pd.DataFrame({"asset": returns, "bench": bench_returns}).dropna()
    active_returns = aligned["asset"] - aligned["bench"]
    te = active_returns.std()
    if annualize:
        te *= np.sqrt(TRADING_DAYS_PER_YEAR)
    return te


def information_ratio(prices: pd.Series, benchmark_prices: pd.Series) -> float:
    """Calculate the Information Ratio (Active Return / Tracking Error)."""
    asset_return = cagr(prices)
    bench_return = cagr(benchmark_prices)
    active_return = asset_return - bench_return
    te = tracking_error(prices, benchmark_prices)
    if te == 0:
        return 0.0
    return active_return / te


def z_score(prices: pd.Series, window: int = 20) -> pd.Series:
    """Calculate the rolling Z-score of prices."""
    _validate_prices(prices, "prices (z-score)")
    roll_mean = prices.rolling(window=window).mean()
    roll_std = prices.rolling(window=window).std()
    return (prices - roll_mean) / roll_std


def hurst_exponent(prices: pd.Series, max_lag: int = 20) -> float:
    """Calculate the Hurst Exponent (measure of mean reversion / trending)."""
    if len(prices) < max_lag * 2:
        return 0.5  # Default to random walk if not enough data

    returns = np.log(prices / prices.shift(1)).dropna()
    lags = range(2, max_lag)
    tau = [np.sqrt(np.std(np.subtract(returns[lag:], returns[:-lag]))) for lag in lags]

    try:
        poly = np.polyfit(np.log(lags), np.log(tau), 1)
        return poly[0] * 2.0
    except Exception:
        return 0.5


def monthly_returns(prices: pd.Series) -> pd.DataFrame:
    monthly = prices.resample("ME").last()
    returns = monthly.pct_change().dropna()
    # Get year and month from DatetimeIndex
    dates = pd.to_datetime(returns.index)
    df = pd.DataFrame(
        {
            "year": dates.year,
            "month": dates.month,
            "return": returns.values,
        }
    )
    pivot = df.pivot(index="year", columns="month", values="return")
    all_months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    # Reindex to ensure all months are present as columns
    present_months = [all_months[i - 1] for i in sorted(df["month"].unique())]
    pivot.columns = pd.Index(present_months)

    # Fill missing months with NaN and ensure order
    for month in all_months:
        if month not in pivot.columns:
            pivot[month] = np.nan

    return pivot[all_months]


def yearly_returns(prices: pd.Series) -> pd.Series:
    yearly = prices.resample("YE").last()
    return yearly.pct_change().dropna()


def correlation_matrix(prices_df: pd.DataFrame) -> pd.DataFrame:
    returns = prices_df.pct_change().dropna()
    return returns.corr()


def detect_regime(
    prices: pd.Series,
    short_window: int = 20,
    long_window: int = 50,
    vol_window: int = 21,
    vol_threshold: float = 0.25,
) -> pd.DataFrame:
    short_ma = prices.rolling(window=short_window).mean()
    long_ma = prices.rolling(window=long_window).mean()
    returns = daily_returns(prices)
    roll_vol = returns.rolling(window=vol_window).std() * np.sqrt(TRADING_DAYS_PER_YEAR)

    trend = pd.Series(index=prices.index, dtype=str)
    trend[short_ma > long_ma] = "uptrend"
    trend[short_ma <= long_ma] = "downtrend"

    volatility_regime = pd.Series(index=prices.index, dtype=str)
    volatility_regime[roll_vol > vol_threshold] = "high_vol"
    volatility_regime[roll_vol <= vol_threshold] = "low_vol"

    regime = pd.DataFrame(
        {
            "trend": trend,
            "volatility_regime": volatility_regime,
            "short_ma": short_ma,
            "long_ma": long_ma,
            "rolling_vol": roll_vol,
        }
    )
    return regime


def value_at_risk(prices: pd.Series, confidence: float = 0.95) -> float:
    """Historical Value at Risk."""
    returns = daily_returns(prices)
    return np.percentile(returns, (1 - confidence) * 100)


def conditional_va_risk(prices: pd.Series, confidence: float = 0.95) -> float:
    """Conditional Value at Risk (Expected Shortfall)."""
    returns = daily_returns(prices)
    var = value_at_risk(prices, confidence)
    return returns[returns <= var].mean()


def omega_ratio(prices: pd.Series, threshold: float = 0.0) -> float:
    """Omega Ratio."""
    returns = daily_returns(prices)
    excess = returns - threshold
    upside = excess[excess > 0].sum()
    downside = -excess[excess < 0].sum()
    return upside / downside if downside != 0 else 0.0


def win_rate(prices: pd.Series) -> float:
    """Percentage of positive days."""
    returns = daily_returns(prices)
    return len(returns[returns > 0]) / len(returns) if len(returns) > 0 else 0.0


def compute_metrics(
    prices: pd.Series,
    benchmark_prices: Optional[pd.Series] = None,
    risk_free_rate: Optional[float] = None,
) -> dict:
    _validate_prices(prices)
    if risk_free_rate is None:
        risk_free_rate = _RISK_FREE_RATE

    metrics = {
        "total_return": total_return(prices),
        "cagr": cagr(prices),
        "volatility": volatility(prices),
        "max_drawdown": max_drawdown(prices),
        "sharpe_ratio": sharpe_ratio(prices, risk_free_rate),
        "sortino_ratio": sortino_ratio(prices, risk_free_rate),
        "calmar_ratio": calmar_ratio(prices),
        "win_rate": win_rate(prices),
        "var_95": value_at_risk(prices, 0.95),
        "cvar_95": conditional_va_risk(prices, 0.95),
        "omega": omega_ratio(prices),
    }

    if benchmark_prices is not None:
        metrics["beta"] = beta(prices, benchmark_prices)
        metrics["alpha"] = alpha(prices, benchmark_prices, risk_free_rate)
        metrics["tracking_error"] = tracking_error(prices, benchmark_prices)
        metrics["info_ratio"] = information_ratio(prices, benchmark_prices)

    return metrics


def format_metrics(metrics: dict) -> dict:
    formatters = {
        "total_return": lambda x: f"{x * 100:.2f}%",
        "cagr": lambda x: f"{x * 100:.2f}%",
        "volatility": lambda x: f"{x * 100:.2f}%",
        "max_drawdown": lambda x: f"{x * 100:.2f}%",
        "sharpe_ratio": lambda x: f"{x:.2f}",
        "sortino_ratio": lambda x: f"{x:.2f}",
        "calmar_ratio": lambda x: f"{x:.2f}",
        "beta": lambda x: f"{x:.2f}",
        "alpha": lambda x: f"{x * 100:.2f}%",
        "tracking_error": lambda x: f"{x * 100:.2f}%",
        "info_ratio": lambda x: f"{x:.2f}",
    }
    return {k: formatters.get(k, lambda x: f"{x:.2f}")(v) for k, v in metrics.items()}


def compute_rolling_metrics(
    prices: pd.Series,
    windows: Optional[dict[str, int]] = None,
) -> pd.DataFrame:
    if windows is None:
        windows = {"volatility": 21, "sharpe": 63}

    result = pd.DataFrame(index=prices.index)
    result["price"] = prices
    result["rolling_vol"] = rolling_volatility(prices, window=windows["volatility"])
    result["rolling_sharpe"] = rolling_sharpe(prices, window=windows["sharpe"])
    result["drawdown"] = drawdown_series(prices)

    return result
