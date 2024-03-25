"""Script which extracts, transforms and loads data from an S3 bucket to Redshift."""

from os import environ
import sys

from boto3 import client
from dotenv import load_dotenv
import pandas as pd
from redshift_connector import Connection

from extract import get_object_keys, get_latest_time, get_latest_truck_data
from transform import remove_non_numerics, convert_total_to_float, remove_negatives
from transform import remove_extremes, convert_payments, TOTAL_LIMIT
from load import get_redshift_connection, QUERY

def extract_data(s3_client: client):
    """Returns the latest truck data from an S3 bucket."""

    latest_time = get_latest_time()

    keys = get_object_keys(s3_client, environ["TRUCK_BUCKET"])

    return get_latest_truck_data(s3_client, environ["TRUCK_BUCKET"], keys, latest_time)


def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """Cleans the truck data ready to be uploaded."""

    data = remove_non_numerics(data)
    data = convert_total_to_float(data)
    data = remove_negatives(data)
    data = remove_extremes(data, TOTAL_LIMIT)
    data = convert_payments(data)

    return data

def load_data(data: pd.DataFrame, db_conn: Connection) -> None:
    """Loads a given number of rows to a database."""

    data_list = data.values.tolist()

    data_to_load = [
        [truck_id, str(at), payment_id, amount]
        for [truck_id, at, payment_id, amount] in data_list
        ]

    with db_conn.cursor() as cur:
        cur.executemany(QUERY, data_to_load)

    db_conn.commit()


if __name__ == "__main__":

    load_dotenv()

    s3 = client("s3",
                aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    try:
        raw_data = extract_data(s3)
    except ValueError:
        print("Error - no data to upload.")
        sys.exit()

    cleaned_data = transform_data(raw_data)

    rs_conn = get_redshift_connection(environ)

    load_data(cleaned_data, rs_conn)
