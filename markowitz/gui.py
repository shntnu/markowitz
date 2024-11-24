import gradio as gr
from .portfolio import MarkowitzPortfolio

# Templates for output messages
SUCCESS_TEMPLATE = """
## ✅ Portfolio Optimization Results

### Weights
{weights}

### Portfolio Metrics (Annualized)
* **Expected Return**: {return_pct:.1%}
* **Risk**: {risk_pct:.1%}
"""

RANGE_ERROR_TEMPLATE = """
## ⚠️ Optimization Error

{error_msg}

Please adjust your target return to be within the feasible range and try again.
"""

ERROR_TEMPLATE = """
## ❌ Error

An unexpected error occurred: {error_msg}
"""


def format_weights(weights):
    """Format portfolio weights into markdown bullet points"""
    return "\n".join(
        f"* **{asset}**: {weight:.1%}" for asset, weight in weights.items()
    )


def optimize_portfolio(csv_file, target_return):
    portfolio = MarkowitzPortfolio()

    try:
        portfolio._load_data(csv_file.name)
        result = portfolio._optimize_weights(target_return / 100)

        return SUCCESS_TEMPLATE.format(
            weights=format_weights(result["weights"]),
            return_pct=result["return"],
            risk_pct=result["risk"],
        )

    except ValueError as e:
        template = (
            RANGE_ERROR_TEMPLATE
            if "feasible range" in str(e).lower()
            else ERROR_TEMPLATE
        )
        return template.format(error_msg=str(e))


def run():
    interface = gr.Interface(
        fn=optimize_portfolio,
        inputs=[
            gr.File(label="Upload Returns CSV file"),
            gr.Slider(
                minimum=1,
                maximum=100,
                step=0.1,
                value=15,
                label="Target Annual Return (%)",
            ),
        ],
        outputs=gr.Markdown(),
        title="Markowitz Portfolio Optimizer",
        description="Upload a CSV with daily returns (must include Date column). Select your target return and optimize your portfolio.",
    )

    interface.launch()


if __name__ == "__main__":
    run()
