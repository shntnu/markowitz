import fire
from .portfolio import MarkowitzPortfolio
from .gui import run as run_gui
from .formatters import format_portfolio_results, format_frontier


class CLI:
    def __init__(self):
        self.portfolio = MarkowitzPortfolio()

    def optimize(self, returns_file: str, target_return: float):
        result = self.portfolio.optimize(returns_file, target_return)
        print(format_portfolio_results(result))

    def gui(self):
        run_gui()


def main():
    fire.Fire(CLI)


if __name__ == "__main__":
    main()
