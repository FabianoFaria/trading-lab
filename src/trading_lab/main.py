import argparse
from pathlib import Path

from trading_lab.backtest import run_backtest
from trading_lab.data import load_prices


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Educational historical-price backtest (simulation only)."
    )
    parser.add_argument("--csv", default="data/sample_prices.csv", help="Path to CSV with date,close columns")
    parser.add_argument("--output", default="reports/backtest_results.csv", help="Path for output CSV")
    parser.add_argument("--short-window", type=int, default=3)
    parser.add_argument("--long-window", type=int, default=5)
    parser.add_argument("--cost-rate", type=float, default=0.001, help="Illustrative cost per turnover; 0.001 = 0.1%%")
    args = parser.parse_args()

    prices = load_prices(args.csv)
    results = run_backtest(
        prices,
        short_window=args.short_window,
        long_window=args.long_window,
        cost_rate=args.cost_rate,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)

    total_return = results["equity"].iloc[-1] - 1.0
    max_drawdown = (results["equity"] / results["equity"].cummax() - 1.0).min()

    print("Trading Lab — backtest educacional (somente simulação)")
    print(f"Linhas processadas: {len(results)}")
    print(f"Retorno acumulado teórico: {total_return:.2%}")
    print(f"Maximum drawdown teórico: {max_drawdown:.2%}")
    print(f"Arquivo de resultados: {output_path}")
    print("Aviso: dados e custos devem ser validados; resultados não são previsão de retorno.")


if __name__ == "__main__":
    main()
