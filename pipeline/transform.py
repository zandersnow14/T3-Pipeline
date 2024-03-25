"""Functions which clean the data."""

import pandas as pd

TOTAL_LIMIT = 100


def remove_non_numerics(data: pd.DataFrame) -> pd.DataFrame:
    """Removes non-numeric values from the 'total' column."""

    return data[pd.to_numeric(data["total"], errors="coerce").notnull()]


def convert_total_to_float(data: pd.DataFrame) -> pd.DataFrame:
    """Converts all values in 'total' column to floats."""

    return data.astype({"total": "float"})


def remove_negatives(data: pd.DataFrame) -> pd.DataFrame:
    """Removes negative values from the 'total' column."""

    return data[data["total"] > 0]


def remove_extremes(data: pd.DataFrame, max_value: int) -> pd.DataFrame:
    """Removes extreme values from the 'total' column."""

    return data[data["total"] < max_value]


def convert_payments(data: pd.DataFrame) -> pd.DataFrame:
    """Changes card/cash values to their ID values (1/2)."""
    data.loc[data['type'] == 'card', 'type'] = 1
    data.loc[data['type'] == 'cash', 'type'] = 2
    return data
