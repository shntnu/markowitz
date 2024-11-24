import gradio as gr
from .portfolio import MarkowitzPortfolio


def optimize_portfolio(csv_file, target_return):
    portfolio = MarkowitzPortfolio()

    # Run optimization
    portfolio.optimize(csv_file.name, target_return / 100)
    result = portfolio._optimize_weights(target_return / 100)

    # Format results
    output = "Portfolio Weights:\n"
    for asset, weight in result["weights"].items():
        output += f"{asset}: {weight:.1%}\n"
    output += f"\nExpected Return: {result['return']:.1%}"
    output += f"\nRisk: {result['risk']:.1%}"

    return output


def run():
    interface = gr.Interface(
        fn=optimize_portfolio,
        inputs=[
            gr.File(label="Returns CSV"),
            gr.Slider(
                minimum=1, maximum=100, step=0.1, value=15, label="Target Return (%)"
            ),
        ],
        outputs="text",
        title="Markowitz Portfolio Optimizer",
        description="Upload a CSV with daily returns and set your target return",
    )
    interface.launch()


if __name__ == "__main__":
    run()
