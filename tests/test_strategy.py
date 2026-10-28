import pandas as pd
import pytest

from trading_lab.strategy import moving_average_signals


def test_strategy_creates_expected_columns_and_binary_signal():
    prices = pd.DataFrame({"close": [10, 11, 12, 13, 14, 15]})

    result = moving_average_signals(prices, short_window=2, long_window=3)

    assert {"sma_short", "sma_long", "signal"}.issubset(result.columns)
    assert set(result["signal"].unique()).issubset({0, 1})
    assert result.loc[0, "signal"] == 0


def test_strategy_rejects_invalid_window_order():
    prices = pd.DataFrame({"close": [10, 11, 12]})

    with pytest.raises(ValueError, match="smaller"):
        moving_average_signals(prices, short_window=5, long_window=3)


def test_strategy_rejects_missing_close_column():
    with pytest.raises(ValueError, match="close"):
        moving_average_signals(pd.DataFrame({"price": [10, 11, 12]}))
