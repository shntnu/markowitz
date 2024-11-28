import pytest
import pandas as pd
import numpy as np
from markowitz.portfolio import MarkowitzPortfolio


@pytest.fixture
def sample_returns():
    """Create sample returns for testing."""
    dates = pd.date_range(start="2024-01-01", end="2024-01-10", freq="D")
    # More realistic daily returns (around 10-15% annualized)
    data = {
        "AAPL": [
            0.001,
            -0.002,
            0.001,
            -0.001,
            0.002,
            0.001,
            -0.001,
            0.002,
            -0.001,
            0.001,
        ],
        "GOOGL": [
            -0.001,
            0.002,
            0.001,
            0.001,
            -0.001,
            -0.001,
            0.001,
            0.001,
            0.002,
            -0.001,
        ],
        "MSFT": [
            0.002,
            0.001,
            -0.001,
            0.001,
            0.001,
            0.001,
            0.001,
            -0.001,
            0.001,
            0.001,
        ],
    }
    return pd.DataFrame(data, index=dates)


def test_load_data(sample_returns):
    """Test data loading from DataFrame and statistics calculation."""
    portfolio = MarkowitzPortfolio()
    portfolio.load_data(sample_returns)

    assert portfolio.returns is not None
    assert portfolio._mean is not None
    assert portfolio._cov is not None
    assert len(portfolio.returns.columns) == 3


def test_optimize_basic(sample_returns):
    """Test basic portfolio optimization."""
    portfolio = MarkowitzPortfolio()

    # Calculate achievable target return
    portfolio.load_data(sample_returns)
    min_ret = portfolio._mean.min() * 252
    max_ret = portfolio._mean.max() * 252
    target = (min_ret + max_ret) / 2  # Use middle of feasible range

    result = portfolio.optimize(sample_returns, target_return=target)

    # Check structure and constraints
    assert set(result.keys()) == {"weights", "return", "risk"}
    assert set(result["weights"].keys()) == set(sample_returns.columns)
    assert np.isclose(sum(result["weights"].values()), 1, rtol=1e-5)
    assert all(0 <= w <= 1 for w in result["weights"].values())


def test_optimize_invalid_return(sample_returns):
    """Test optimization with unreachable target return."""
    portfolio = MarkowitzPortfolio()
    portfolio.load_data(sample_returns)
    max_ret = portfolio._mean.max() * 252

    with pytest.raises(ValueError):
        portfolio.optimize(
            sample_returns, target_return=max_ret * 2
        )  # Double the maximum possible


def test_portfolio_calculations(sample_returns):
    """Test internal portfolio calculations."""
    portfolio = MarkowitzPortfolio()
    portfolio.load_data(sample_returns)

    weights = np.array([0.4, 0.3, 0.3])
    variance = portfolio._portfolio_variance(weights)
    ret = portfolio._portfolio_return(weights)

    assert isinstance(variance, float)
    assert isinstance(ret, float)
    assert variance >= 0  # Variance must be non-negative
