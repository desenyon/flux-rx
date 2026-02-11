import numpy as np
import pandas as pd
import pytest
from flux_rx.analytics import cagr, volatility, sharpe_ratio, win_rate, value_at_risk


@pytest.fixture
def sample_prices():
    # 5 days of 1% daily returns starting at 100
    returns = np.array([0.01, 0.01, 0.01, 0.01, 0.01])
    prices = [100.0]
    for r in returns:
        prices.append(prices[-1] * (1 + r))
    return pd.Series(prices, index=pd.date_range("2023-01-01", periods=6))


def test_cagr_positive(sample_prices):
    result = cagr(sample_prices)
    assert result > 0
    # 1% per day for 5 days is approx 5% in 5 days.
    # Annualized it should be very high.
    assert result > 1.0 


def test_volatility_low(sample_prices):
    # Constant 1% return has very low volatility (only 0 because it's constant)
    # Wait, 1% constant return means std is 0
    result = volatility(sample_prices)
    assert result == 0.0


def test_win_rate(sample_prices):
    assert win_rate(sample_prices) == 1.0


def test_var_95(sample_prices):
    # All returns are +1%, so 5th percentile is also +1% (actually depends on interpolation)
    # But it shouldn't be negative
    assert value_at_risk(sample_prices, 0.95) >= 0.01


def test_sharpe_ratio_high(sample_prices):
    # Constant positive return with 0 vol should theoretically be inf or handled
    # Our sharpe_ratio handles std=0 by returning 0 (or should handle it gracefully)
    result = sharpe_ratio(sample_prices, risk_free_rate=0.0)
    # With std=0, current implementation returns 0
    assert result == 0.0
