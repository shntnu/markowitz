import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict, Union, List, Tuple


class MarkowitzPortfolio:
    """Implements Markowitz Portfolio Optimization.

    Finds minimum variance portfolios for given target returns,
    assuming no short-selling and full investment constraints.
    """

    def __init__(self):
        self.returns = None
        self._mean = None
        self._cov = None

    def load_data(self, returns_data: Union[str, pd.DataFrame]) -> None:
        """Load and process returns data for portfolio optimization.

        Args:
            returns_data (Union[str, pd.DataFrame]): CSV file path or DataFrame
                with returns data. Must have Date index and asset returns in columns.
        """
        self.returns = (
            pd.read_csv(returns_data, index_col="Date", parse_dates=True)
            if isinstance(returns_data, str)
            else returns_data
        )
        self._mean = self.returns.mean()
        self._cov = self.returns.cov()

    def _portfolio_variance(self, weights: np.ndarray) -> float:
        """Calculate portfolio variance.

        Args:
            weights (np.ndarray): Array of asset weights

        Returns:
            float: Portfolio variance (not annualized)
        """
        return weights @ self._cov @ weights

    def _portfolio_return(self, weights: np.ndarray) -> float:
        """Calculate portfolio return.

        Args:
            weights (np.ndarray): Array of asset weights

        Returns:
            float: Portfolio return (not annualized)
        """
        return weights @ self._mean

    def _optimize_weights(self, target_return: float) -> Dict:
        """Find optimal portfolio weights for target return.

        Args:
            target_return (float): Target annual return (decimal)

        Returns:
            Dict: Dictionary containing:
                weights (Dict[str, float]): Asset weights
                return (float): Annualized return
                risk (float): Annualized risk

        Raises:
            ValueError: If optimization fails
        """
        n_assets = len(self.returns.columns)
        daily_target = target_return / 252

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
        )

        if not result.success:
            raise ValueError(f"Optimization failed: {result.message}")

        return {
            "weights": dict(zip(self.returns.columns, result.x)),
            "return": float(self._portfolio_return(result.x) * 252),
            "risk": float(np.sqrt(self._portfolio_variance(result.x) * 252)),
        }

    def optimize(
        self, returns_data: Union[str, pd.DataFrame], target_return: float
    ) -> Dict:
        """Load data and optimize portfolio in one step.

        Args:
            returns_data (Union[str, pd.DataFrame]): CSV file path or DataFrame with returns data
            target_return (float): Target annual return (decimal)

        Returns:
            Dict: Dictionary containing optimal weights, annualized return and risk
        """
        self.load_data(returns_data)
        return self._optimize_weights(target_return)

    def efficient_frontier(
        self, returns_data: Union[str, pd.DataFrame], points: int = 50
    ) -> List[Tuple[float, float]]:
        """Generate points along the efficient frontier.

        Args:
            returns_data (Union[str, pd.DataFrame]): CSV file path or DataFrame with returns data
            points (int, optional): Number of points to generate. Defaults to 50.

        Returns:
            List[Tuple[float, float]]: List of (return, risk) tuples along the frontier
        """
        self.load_data(returns_data)

        min_ret = self._mean.min() * 252
        max_ret = self._mean.max() * 252
        target_returns = np.linspace(min_ret, max_ret, points)
        ef_points = []

        for target in target_returns:
            try:
                result = self._optimize_weights(target)
                ef_points.append((result["return"], result["risk"]))
            except ValueError:
                continue

        return ef_points
