import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict
import sys


class MarkowitzPortfolio:
    """Markowitz Portfolio Optimization."""

    def __init__(self):
        self.returns = None
        self._mean = None
        self._cov = None

    def _load_data(self, returns_file: str) -> None:
        """Load and prepare returns data."""
        try:
            self.returns = pd.read_csv(returns_file, index_col="Date", parse_dates=True)
            # Keep raw daily stats, don't annualize yet
            self._mean = self.returns.mean()
            self._cov = self.returns.cov()
        except Exception as e:
            sys.exit(f"Error reading returns file: {e}")

    def _portfolio_variance(self, weights: np.ndarray) -> float:
        """Calculate portfolio variance."""
        return weights @ self._cov @ weights

    def _portfolio_return(self, weights: np.ndarray) -> float:
        """Calculate portfolio return."""
        return weights @ self._mean

    def _optimize_weights(self, target_return: float) -> Dict:
        """Find optimal weights for target return."""
        n_assets = len(self.returns.columns)

        # Convert annual target return to daily
        daily_target = target_return / 252

        # Check if target return is feasible
        min_ret = self._mean.min()
        max_ret = self._mean.max()
        if daily_target < min_ret or daily_target > max_ret:
            raise ValueError(
                f"Target return of {target_return:.1%} annual ({daily_target:.3%} daily) "
                f"is not feasible. Feasible range: {min_ret*252:.1%} to {max_ret*252:.1%} annual"
            )

        constraints = [
            {"type": "eq", "fun": lambda w: self._portfolio_return(w) - daily_target},
            {"type": "eq", "fun": lambda w: np.sum(w) - 1},
        ]
        bounds = tuple((0, 1) for _ in range(n_assets))

        result = minimize(
            self._portfolio_variance,
            x0=np.ones(n_assets) / n_assets,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
            options={"ftol": 1e-9, "maxiter": 1000},
        )

        if not result.success:
            raise ValueError(f"Optimization failed: {result.message}")

        variance = self._portfolio_variance(result.x)
        return {
            "weights": dict(zip(self.returns.columns, result.x)),
            "return": self._portfolio_return(result.x) * 252,  # Annualize
            "risk": np.sqrt(variance * 252),  # Annualize
        }

    def optimize(self, returns_file: str, target_return: float) -> None:
        """Find minimum variance portfolio for target return."""
        self._load_data(returns_file)

        try:
            # Convert target_return from percentage to decimal if needed
            if target_return > 1:
                target_return = target_return / 100

            result = self._optimize_weights(target_return)

            print("\nOptimal Portfolio:")
            for asset, weight in result["weights"].items():
                print(f"{asset}: {weight:.2%}")
            print("\nPortfolio Metrics (Annualized):")
            print(f"Expected Return: {result['return']:.2%}")
            print(f"Volatility: {result['risk']:.2%}")

        except Exception as e:
            sys.exit(f"Optimization error: {e}")

    def efficient_frontier(self, returns_file: str, points: int = 50) -> None:
        """Generate and display efficient frontier."""
        self._load_data(returns_file)

        # Get feasible return range
        min_ret = self._mean.min() * 252  # Annualize
        max_ret = self._mean.max() * 252  # Annualize

        target_returns = np.linspace(min_ret, max_ret, points)
        ef_points = []

        print("\nGenerating Efficient Frontier...")
        print(f"Return range: {min_ret:.1%} to {max_ret:.1%} (annual)")

        for target in target_returns:
            try:
                result = self._optimize_weights(target)
                ef_points.append((result["return"], result["risk"]))
            except ValueError:
                continue

        if ef_points:
            print("\nEfficient Frontier Points (Annualized):")
            print("Return    Risk")
            print("-" * 20)
            for ret, risk in ef_points:
                print(f"{ret:7.2%}  {risk:7.2%}")
        else:
            print("No feasible portfolios found.")
