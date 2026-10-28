import pandas as pd
import pytest

from trading_lab.data import load_prices


def test_load_prices_sorts_dates_and_normalizes_headers(tmp_path):
    csv = tmp_path / "prices.csv"
    csv.write_text("Date,Close\n2025-01-03,11\n2025-01-02,10\n", encoding="utf-8")

    result = load_prices(csv)

    assert list(result.columns) == ["date", "close"]
    assert result["date"].tolist() == [
        pd.Timestamp("2025-01-02"),
        pd.Timestamp("2025-01-03"),
    ]


def test_load_prices_rejects_non_positive_prices(tmp_path):
    csv = tmp_path / "prices.csv"
    csv.write_text("date,close\n2025-01-02,10\n2025-01-03,0\n", encoding="utf-8")

    with pytest.raises(ValueError, match="greater than zero"):
        load_prices(csv)


def test_load_prices_rejects_duplicate_dates(tmp_path):
    csv = tmp_path / "prices.csv"
    csv.write_text("date,close\n2025-01-02,10\n2025-01-02,11\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate dates"):
        load_prices(csv)


def test_load_prices_rejects_missing_columns(tmp_path):
    csv = tmp_path / "prices.csv"
    csv.write_text("date,open\n2025-01-02,10\n2025-01-03,11\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Missing required"):
        load_prices(csv)
