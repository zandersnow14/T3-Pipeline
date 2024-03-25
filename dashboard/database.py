"""Utility functions for the database."""

from os import _Environ

from redshift_connector import connect, Connection
import pandas as pd


def get_database_connection(config: _Environ) -> Connection:
    """Returns a connection to database."""

    return connect(host=config["DB_HOST"],
        port=config["DB_PORT"],
        database=config["DB_NAME"],
        user=config["DB_USERNAME"],
        password=config["DB_PASSWORD"]
    )


def load_transaction_data(db_conn: Connection) -> pd.DataFrame:
    """Returns dataframe of transactions."""

    query = """SELECT tran.truck_id, truck.name, tran.at, pay.type, tran.amount
               FROM zander_schema.fact_transactions AS tran
               JOIN zander_schema.dim_payments AS pay ON tran.payment_id = pay.id
               JOIN zander_schema.dim_trucks AS truck ON truck.id = tran.truck_id;"""

    with db_conn.cursor() as cur:
        cur.execute(query)
        return cur.fetch_dataframe()
    