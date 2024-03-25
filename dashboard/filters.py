"""Functions for filtering data."""

from datetime import datetime, timedelta

import pandas as pd

def filter_by_date(data: pd.DateOffset, range_of_dates: tuple[datetime]) -> pd.DataFrame:
    """Returns data within the given date range."""

    condition = (data['at'] >= str(range_of_dates[0])) & (data['at'] <= str(range_of_dates[1] + timedelta(days=1)))

    return data.loc[condition]

def filter_by_truck(data: pd.DataFrame, trucks: list[str]) -> pd.DataFrame:
    """Returns data about the given trucks."""

    return data[data['name'].isin(trucks)]
