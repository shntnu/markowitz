import gradio as gr
from .portfolio import MarkowitzPortfolio
from .formatters import format_portfolio_results


def optimize_portfolio(csv_file, target_return):
    """Process portfolio optimization request from GUI.

    Args:
        csv_file: Gradio file object containing returns data
        target_return: Target return percentage (1-100)

    Returns:
        str: Markdown formatted results or error message
    """
    portfolio = MarkowitzPortfolio()
    try:
        result = portfolio.optimize(csv_file.name, target_return / 100)
        return format_portfolio_results(result, markdown=True)
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def run():
    """Launch the Gradio interface."""
    interface = gr.Interface(
        fn=optimize_portfolio,
        inputs=[
            gr.File(
                label="Upload Returns CSV file",
                file_types=[".csv"],  # Added file type restriction
            ),
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
