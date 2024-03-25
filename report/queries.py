"""Functions which query a Pandas dataframe for key metrics."""

import pandas as pd

def get_trucks_by_count(data: pd.DataFrame) -> dict:
    """Returns the trucks and their counts in des."""

    return data.groupby('name').amount.agg('count').sort_values(ascending=False).to_dict()


def get_trucks_by_value(data: pd.DataFrame) -> dict:
    """Returns the trucks and their total transaction values."""

    output = data.groupby('name').amount.agg('sum').sort_values(ascending=False).to_dict()

    return {k:round(v, 2) for (k, v) in output.items()}




def get_trucks_by_avg_amount(data: pd.DataFrame) -> dict:
    """Returns the trucks and their counts in des."""

    output = data.groupby('name').amount.agg('mean').sort_values(ascending=False).to_dict()

    return {k:round(v, 2) for (k, v) in output.items()}


def get_total_transaction_value(data: pd.DataFrame) -> float:
    """Returns total transaction value from the data."""

    return round(data['amount'].sum(), 2)


def get_best_hour_trucks(data: pd.DataFrame) -> dict:
    """Returns the trucks and their most popular hour of the day."""

    new_data = data.copy()

    new_data['at'] = new_data['at'].dt.hour

    output = new_data.groupby(['name', 'at']).count().sort_values(by='amount').groupby(level=0).tail(1)

    output = output.rename(columns={'truck_id': 'count'}).drop(columns=['type', 'amount']).sort_values(by='count', ascending=False)

    output = output.to_dict()['count']

    return {k[0]: {"hour": k[1], "transactions": v} for (k, v) in output.items()}
