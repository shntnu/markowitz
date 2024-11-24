import pandas as pd
import numpy as np


def generate_sample_returns():
    # Set seed for reproducibility
    np.random.seed(42)

    # Define parameters for different assets (adjusted for more realistic daily values)
    assets = {
        "AAPL": {"mean": 0.0007, "std": 0.008},  # ~17.5% annual return, ~13% vol
        "GOOGL": {"mean": 0.0006, "std": 0.007},  # ~15% annual return, ~11% vol
        "MSFT": {"mean": 0.0007, "std": 0.007},  # ~17.5% annual return, ~11% vol
        "BRK.B": {"mean": 0.0005, "std": 0.006},  # ~12.5% annual return, ~10% vol
        "VOO": {"mean": 0.0004, "std": 0.005},  # ~10% annual return, ~8% vol
    }

    # Rest of the code remains the same...
    dates = pd.date_range(
        start="2023-01-01",
        end="2023-12-31",
        freq="B",  # Business days
    )

    rho = np.array(
        [
            [1.0, 0.6, 0.5, 0.4, 0.7],
            [0.6, 1.0, 0.7, 0.3, 0.6],
            [0.5, 0.7, 1.0, 0.3, 0.6],
            [0.4, 0.3, 0.3, 1.0, 0.5],
            [0.7, 0.6, 0.6, 0.5, 1.0],
        ]
    )

    L = np.linalg.cholesky(rho)
    n_days = len(dates)
    n_assets = len(assets)

    Z = np.random.standard_normal((n_days, n_assets))
    X = Z @ L.T

    returns_data = pd.DataFrame(index=dates, columns=assets.keys())

    for i, (asset, params) in enumerate(assets.items()):
        returns_data[asset] = (X[:, i] * params["std"]) + params["mean"]

    returns_data = returns_data.round(6)
    returns_data.reset_index(inplace=True)
    returns_data.rename(columns={"index": "Date"}, inplace=True)

    return returns_data


# Generate and save the data
returns = generate_sample_returns()
returns.to_csv("sample_returns.csv", index=False)

# Print sample statistics
print("\nSample Returns Statistics (Annualized):")
print("\nReturns:")
print((returns.set_index("Date").mean() * 252 * 100).round(2).astype(str) + "%")
print("\nVolatility:")
print((returns.set_index("Date").std() * np.sqrt(252) * 100).round(2).astype(str) + "%")

# Print first few rows
print("\nFirst few rows of returns (as percentages):")
print(
    pd.concat(
        [
            returns["Date"],
            (returns.drop("Date", axis=1) * 100).round(3).astype(str) + "%",
        ],
        axis=1,
    ).head()
)
