# Flux-RX Portfolio Module: Portfolio optimization and analysis
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Optional, Union, Dict


def optimize_portfolio(
    prices: pd.DataFrame,
    objective: str = "sharpe",  # "sharpe", "min_vol", "max_return"
    risk_free_rate: float = 0.04,
) -> Dict[str, Union[float, Dict[str, float]]]:
    """
    Perform portfolio optimization using Mean-Variance analysis.
    """
    returns = prices.pct_change().dropna()
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    num_assets = len(prices.columns)
    
    def portfolio_performance(weights):
        port_return = np.sum(mean_returns * weights)
        port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return port_return, port_std

    def neg_sharpe_ratio(weights):
        p_return, p_std = portfolio_performance(weights)
        return -(p_return - risk_free_rate) / p_std

    def portfolio_volatility(weights):
        return portfolio_performance(weights)[1]

    def portfolio_return(weights):
        return -portfolio_performance(weights)[0]

    constraints = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    initial_weights = [1.0 / num_assets] * num_assets
    
    if objective == "sharpe":
        result = minimize(neg_sharpe_ratio, initial_weights, bounds=bounds, constraints=constraints)
    elif objective == "min_vol":
        result = minimize(portfolio_volatility, initial_weights, bounds=bounds, constraints=constraints)
    elif objective == "max_return":
        result = minimize(portfolio_return, initial_weights, bounds=bounds, constraints=constraints)
    else:
        raise ValueError(f"Unknown objective: {objective}")
        
    opt_weights = result.x
    opt_return, opt_std = portfolio_performance(opt_weights)
    
    return {
        "return": opt_return,
        "volatility": opt_std,
        "sharpe_ratio": (opt_return - risk_free_rate) / opt_std,
        "weights": dict(zip(prices.columns, opt_weights))
    }


def equal_weight_portfolio(prices: pd.DataFrame) -> Dict[str, Union[float, Dict[str, float]]]:
    """Calculate performance for an equal-weighted portfolio."""
    num_assets = len(prices.columns)
    weights = np.array([1.0 / num_assets] * num_assets)
    
    returns = prices.pct_change().dropna()
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    
    port_return = np.sum(mean_returns * weights)
    port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    return {
        "return": port_return,
        "volatility": port_std,
        "weights": dict(zip(prices.columns, weights))
    }
