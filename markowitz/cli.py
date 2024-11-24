import fire
from .portfolio import MarkowitzPortfolio
from .gui import run as run_gui


class MarkowitzCLI:
    """Markowitz Portfolio Optimization CLI"""

    def __init__(self):
        self.portfolio = MarkowitzPortfolio()

    def optimize(self, returns_file: str, target_return: float) -> None:
        """Find minimum variance portfolio for target return."""
        self.portfolio.optimize(returns_file, target_return)

    def efficient_frontier(self, returns_file: str, points: int = 50) -> None:
        """Generate and display efficient frontier."""
        self.portfolio.efficient_frontier(returns_file, points)

    def gui(self) -> None:
        """Launch the web interface."""
        run_gui()


def main():
    fire.Fire(MarkowitzCLI)


if __name__ == "__main__":
    main()
