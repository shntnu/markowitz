# Markowitz Portfolio Optimizer

A command-line tool for portfolio optimization using Modern Portfolio Theory (MPT). Calculate optimal asset allocations and generate efficient frontiers based on historical returns data.

## Installation

This project uses Poetry for dependency management. To install:

```bash
# Clone the repository
git clone [your-repo-url]
cd markowitz

# Install dependencies
poetry install
```

## Usage

The tool provides two main commands: `optimize` and `efficient_frontier`.

### Optimize a Portfolio

Find the minimum variance portfolio for a target return:

```bash
poetry run markowitz optimize --returns-file sample_returns.csv --target-return 15
```

This will output optimal weights for each asset and portfolio metrics (return and risk).

### Generate Efficient Frontier

View the risk-return tradeoff across different target returns:

```bash
poetry run markowitz efficient_frontier --returns-file sample_returns.csv --points 50
```

## Data Format

The tool expects a CSV file with daily returns in the following format:

```csv
Date,AAPL,GOOGL,MSFT,BRK.B,VOO
2023-01-01,0.0007,-0.0003,0.0005,0.0002,0.0004
...
```

A sample data generator script is provided in `scripts/sample-data-generator.py`.

## Features

- Portfolio optimization using mean-variance analysis
- Efficient frontier generation
- No-short-selling constraint
- Annualized risk and return metrics
- Support for multiple assets
- Built-in sample data generation

## Dependencies

- Python ≥ 3.11
- NumPy
- Pandas
- SciPy
- Python Fire (CLI interface)

## Development

Run tests with:

```bash
poetry run pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.