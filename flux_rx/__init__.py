# Flux-RX: A Finance Python Package
from flux_rx.api import quick, chart, compare, app, metrics, info, help_api, export, optimize, screen
# ... existing data imports ...
from flux_rx.data import fetch, fetch_multiple, get_info, clear_cache, get_benchmark_data, align_dataframes, normalize_prices
# ... existing analytics imports ...
from flux_rx.analytics import (
    daily_returns,
    cumulative_returns,
    total_return,
    cagr,
    volatility,
    max_drawdown,
    drawdown_series,
    sharpe_ratio,
    sortino_ratio,
    calmar_ratio,
    rolling_volatility,
    rolling_sharpe,
    rolling_beta,
    beta,
    alpha,
    monthly_returns,
    yearly_returns,
    compute_metrics,
    format_metrics,
    compute_rolling_metrics,
    detect_regime,
    set_risk_free_rate,
    get_risk_free_rate,
)
from flux_rx.charts import (
    price_chart,
    volume_chart,
    drawdown_chart,
    rolling_vol_chart,
    rolling_sharpe_chart,
    monthly_heatmap,
    performance_chart,
    risk_return_scatter,
    correlation_matrix,
    cumulative_returns_chart,
    candlestick_chart,
)
from flux_rx.report import generate_report, generate_comparison_report
from flux_rx.themes import get_theme, apply_theme, list_themes, DEFAULT_THEME
from flux_rx.compare import compare_tickers, ComparisonResult, portfolio_metrics, optimal_weights_minvol, rolling_correlation, sector_exposure, diversification_ratio, performance_attribution
from flux_rx.portfolio import optimize_portfolio, equal_weight_portfolio
from flux_rx.screener import screen_tickers

__version__ = "1.0.0"
__all__ = [
    "quick", "chart", "compare", "app", "metrics", "info", "help_api", "export", "optimize", "screen",
    "fetch", "fetch_multiple", "get_info", "clear_cache", "get_benchmark_data", "align_dataframes", "normalize_prices",
    "daily_returns", "cumulative_returns", "total_return", "cagr", "volatility", "max_drawdown",
    "drawdown_series", "sharpe_ratio", "sortino_ratio", "calmar_ratio", "rolling_volatility",
    "rolling_sharpe", "rolling_beta", "beta", "alpha", "monthly_returns", "yearly_returns",
    "compute_metrics", "format_metrics", "compute_rolling_metrics", "detect_regime",
    "set_risk_free_rate", "get_risk_free_rate",
    "price_chart", "volume_chart", "drawdown_chart", "rolling_vol_chart", "rolling_sharpe_chart",
    "monthly_heatmap", "performance_chart", "risk_return_scatter", "correlation_matrix",
    "cumulative_returns_chart", "candlestick_chart", "generate_report", "generate_comparison_report",
    "get_theme", "apply_theme", "list_themes", "DEFAULT_THEME", "compare_tickers", "ComparisonResult",
    "portfolio_metrics", "optimal_weights_minvol", "rolling_correlation", "sector_exposure",
    "diversification_ratio", "performance_attribution", "optimize_portfolio", "equal_weight_portfolio",
    "screen_tickers",
]
