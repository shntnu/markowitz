def format_portfolio_results(result, markdown=False):
    """Format portfolio optimization results"""
    weights = result["weights"]
    ret = result["return"]
    risk = result["risk"]

    if markdown:
        weights_str = "\n".join(
            f"* **{asset}**: {weight:.1%}" for asset, weight in weights.items()
        )
        return f"""
## Portfolio Results
### Weights
{weights_str}

### Metrics (Annualized)
* **Return**: {ret:.1%}
* **Risk**: {risk:.1%}
"""
    else:
        weights_str = "\n".join(
            f"{asset}: {weight:.2%}" for asset, weight in weights.items()
        )
        return f"""
Optimal Portfolio:
{weights_str}

Portfolio Metrics (Annualized):
Expected Return: {ret:.2%}
Volatility: {risk:.2%}
"""
