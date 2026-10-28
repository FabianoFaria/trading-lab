import pandas as pd


def moving_average_signals(
    prices: pd.DataFrame,
    short_window: int = 3,
    long_window: int = 5,
) -> pd.DataFrame:
    """Return moving averages and a 0/1 desired position signal.

    The signal is calculated using each row's closing price. The backtest
    must delay execution until a later bar to avoid look-ahead bias.
    """
    if short_window < 1 or long_window < 1:
        raise ValueError("Moving-average windows must be positive integers.")
    if short_window >= long_window:
        raise ValueError("short_window must be smaller than long_window.")
    if "close" not in prices.columns:
        raise ValueError("Input data must contain a 'close' column.")

    result = prices.copy()
    result["sma_short"] = result["close"].rolling(
        window=short_window, min_periods=short_window
    ).mean()
    result["sma_long"] = result["close"].rolling(
        window=long_window, min_periods=long_window
    ).mean()

    result["signal"] = (
        (result["sma_short"] > result["sma_long"])
        .fillna(False)
        .astype(int)
    )
    return result
