from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"date", "close"}


def load_prices(csv_path: str | Path) -> pd.DataFrame:
    """Load and validate historical close prices from a CSV file."""
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")

    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns.str.strip().str.lower())
    if missing:
        raise ValueError(f"Missing required CSV columns: {sorted(missing)}")

    # Normalize column names so Date/Close are accepted as well.
    df.columns = [str(column).strip().lower() for column in df.columns]
    df = df.loc[:, ["date", "close"]].copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    if df["date"].isna().any():
        raise ValueError("Column 'date' contains missing or invalid dates.")
    if df["close"].isna().any():
        raise ValueError("Column 'close' contains missing or non-numeric prices.")
    if (df["close"] <= 0).any():
        raise ValueError("All closing prices must be greater than zero.")
    if df["date"].duplicated().any():
        raise ValueError("Duplicate dates are not allowed.")

    df = df.sort_values("date").reset_index(drop=True)
    if len(df) < 2:
        raise ValueError("At least two rows of prices are required.")

    return df
