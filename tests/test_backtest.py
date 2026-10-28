import pandas as pd
import pytest

from trading_lab.backtest import run_backtest


def test_backtest_delays_execution_until_next_bar():
    prices = pd.DataFrame(
        {
            "date": pd.date_range("2025-01-01", periods=6, freq="D"),
            "close": [10, 10, 10, 12, 13, 14],
        }
    )

    result = run_backtest(prices, short_window=2, long_window=3, cost_rate=0)

    # The signal uses the current close; position changes only on the next row.
    assert result.loc[2, "signal"] == 0
    assert result.loc[3, "signal"] == 1
    assert result.loc[3, "position"] == result.loc[2, "signal"]


def test_backtest_charges_cost_when_position_changes():
    prices = pd.DataFrame(
        {
            "date": pd.date_range("2025-01-01", periods=6, freq="D"),
            "close": [10, 10, 10, 12, 13, 14],
        }
    )

    result = run_backtest(prices, short_window=2, long_window=3, cost_rate=0.001)

    assert (result["transaction_cost"] >= 0).all()
    assert (result.loc[result["turnover"] > 0, "transaction_cost"] > 0).all()


def test_backtest_rejects_invalid_cost_rate():
    prices = pd.DataFrame({"close": [10, 11, 12, 13, 14]})

    with pytest.raises(ValueError, match="cost_rate"):
        run_backtest(prices, cost_rate=1.0)
