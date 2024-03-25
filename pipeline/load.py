"""Functions to load truck data to a redshift cluster."""

from os import _Environ

import redshift_connector
import pandas as pd

QUERY="""
INSERT INTO zander_schema.fact_transactions (truck_id, at, payment_id, amount)
    VALUES (%s, %s, %s, %s);
"""

def get_redshift_connection(config: _Environ) -> redshift_connector.Connection:
    """Gets a connection to a redshift cluster."""

    return redshift_connector.connect(
        host=config["DB_HOST"],
        port=config["DB_PORT"],
        database=config["DB_NAME"],
        user=config["DB_USERNAME"],
        password=config["DB_PASSWORD"]
    )

def get_sample_of_data(data: pd.DataFrame, number_of_rows: int) -> pd.DataFrame:
    """Returns a sample of the data to insert into the database."""

    sample = data.sample(number_of_rows).values.tolist()

    return [
        [truck_id, str(at), payment_id, amount]
        for [truck_id, at, payment_id, amount] in sample
        ]
    