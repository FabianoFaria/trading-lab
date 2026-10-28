import pandas as pd

from trading_lab.strategy import moving_average_signals


def run_backtest(
    prices: pd.DataFrame,
    short_window: int = 3,
    long_window: int = 5,
    cost_rate: float = 0.001,
) -> pd.DataFrame:
    """Run a long-or-flat moving-average backtest with delayed execution.

    `cost_rate` is a fractional cost charged on each unit of position turnover.
    Example: 0.001 means 0.1% of notional per full entry or exit.

    This is a simplified educational model, not a broker execution simulator.
    """
    if not 0 <= cost_rate < 1:
        raise ValueError("cost_rate must be in the range [0, 1).")

    result = moving_average_signals(
        prices, short_window=short_window, long_window=long_window
    )

    # A signal known at close t is executed at close t+1.
    result["position"] = result["signal"].shift(1).fillna(0).astype(int)

    # Position held after the prior close earns the return to the current close.
    result["market_return"] = result["close"].pct_change().fillna(0.0)
    result["held_position"] = result["position"].shift(1).fillna(0).astype(int)
    result["turnover"] = result["position"].diff().abs()
    if len(result):
        result.loc[result.index[0], "turnover"] = abs(result["position"].iloc[0])
    result["turnover"] = result["turnover"].fillna(0.0)

    result["transaction_cost"] = result["turnover"] * cost_rate
    result["strategy_return"] = (
        result["market_return"] * result["held_position"]
        - result["transaction_cost"]
    )
    result["equity"] = (1.0 + result["strategy_return"]).cumprod()

    return result
