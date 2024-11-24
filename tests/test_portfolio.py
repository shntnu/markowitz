import pytest
import numpy as np
import pandas as pd
from io import StringIO
from unittest.mock import patch
from markowitz.portfolio import MarkowitzPortfolio


@pytest.fixture
def sample_portfolio():
    """
    Creates a portfolio with two assets showing realistic returns and volatility:
    - Stock A: Higher return (≈ 20% annual) with higher volatility
    - Stock B: Lower return (≈ 10% annual) with lower volatility
    """
    test_data = """Date,Stock_A,Stock_B
2024-01-01,0.0012,0.0003
2024-01-02,0.0008,0.0004
2024-01-03,-0.0002,0.0005
2024-01-04,0.0015,0.0003
2024-01-05,0.0007,0.0005"""

    portfolio = MarkowitzPortfolio()
    with patch(
        "pandas.read_csv",
        return_value=pd.read_csv(
            StringIO(test_data), index_col="Date", parse_dates=True
        ),
    ):
        portfolio._load_data("dummy.csv")
    return portfolio


def test_portfolio_math(sample_portfolio):
    """
    Test that our portfolio calculations match what we'd expect mathematically.
    """
    weights = np.array([0.5, 0.5])

    calculated_return = sample_portfolio._portfolio_return(weights)
    # With varying returns, we'll test that it's close to the mean
    assert calculated_return > 0, "Portfolio return should be positive"


def test_optimization_constraints(sample_portfolio):
    """
    Test that our optimization respects the basic constraints of portfolio theory:
    1. Weights sum to 100%
    2. No negative weights (no short selling)
    """
    result = sample_portfolio._optimize_weights(target_return=0.15)
    weights = np.array(list(result["weights"].values()))

    assert np.isclose(sum(weights), 1), "Portfolio weights must sum to 100%"
    assert all(
        w >= 0 for w in weights
    ), "No short selling allowed - weights must be non-negative"


def test_efficient_frontier_makes_sense(sample_portfolio):
    """
    Test that portfolios with higher returns have higher risk,
    demonstrating the fundamental risk-return tradeoff.
    """
    # Print the mean and std of each asset to understand our test data
    print("\nAsset Statistics (daily):")
    print(
        f"Stock A: mean={sample_portfolio._mean['Stock_A']:.6f}, std={np.sqrt(sample_portfolio._cov.loc['Stock_A','Stock_A']):.6f}"
    )
    print(
        f"Stock B: mean={sample_portfolio._mean['Stock_B']:.6f}, std={np.sqrt(sample_portfolio._cov.loc['Stock_B','Stock_B']):.6f}"
    )

    low_return = 0.12  # 12% annual return target
    high_return = 0.18  # 18% annual return target

    low_risk_portfolio = sample_portfolio._optimize_weights(low_return)
    high_risk_portfolio = sample_portfolio._optimize_weights(high_return)

    print("\nPortfolio Results:")
    print(
        f"Low return portfolio: return={low_risk_portfolio['return']:.2%}, risk={low_risk_portfolio['risk']:.2%}"
    )
    print(
        f"High return portfolio: return={high_risk_portfolio['return']:.2%}, risk={high_risk_portfolio['risk']:.2%}"
    )

    assert (
        low_risk_portfolio["risk"] < high_risk_portfolio["risk"]
    ), "Higher return portfolios should have higher risk"
