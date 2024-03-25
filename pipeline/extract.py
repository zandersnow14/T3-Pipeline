"""Functions to retrieve the latest truck data from an S3 bucket."""

from io import StringIO
from datetime import datetime

from boto3 import client
import pandas as pd

CURRENT_DATETIME = datetime.now()


def get_latest_time() -> str:
    """Returns the datetime when the latest files could have been uploaded."""

    current_hour = CURRENT_DATETIME.hour
    latest_hour = current_hour - current_hour % 3
    new_datetime = CURRENT_DATETIME.replace(hour=latest_hour)

    return new_datetime.strftime("%Y-%m/%d/%H")


def get_object_keys(s3_client: client, bucket: str) -> list [str]:
    """Return list of all object keys in a given bucket."""

    contents = s3_client.list_objects(Bucket=bucket)["Contents"]

    return [obj["Key"] for obj in contents]


def get_csv_from_obj(obj: dict) -> str:
    """Returns a csv string from a given object."""

    obj_body = obj['Body']
    return obj_body.read().decode('utf-8')

def get_truck_df_from_csv(csv_string: str, truck_id: int) -> pd.DataFrame:
    """Returns the truck dataframe with the truck_id from the given csv string."""

    truck_df = pd.read_csv(StringIO(csv_string))
    truck_df.insert(0, "truck_id", truck_id)

    return truck_df


def get_latest_truck_data(s3_client: client, bucket: str, obj_keys: list[str], latest_time: str) -> pd.DataFrame:
    """Returns the combined truck data from the latest files in the S3 bucket."""

    data = []
    for key in obj_keys:
        if latest_time in key:
            obj = s3_client.get_object(Bucket=bucket, Key=key)

            csv_string = get_csv_from_obj(obj)

            truck_id = key[-8]

            truck_df = get_truck_df_from_csv(csv_string, truck_id)

            data.append(truck_df)

    return pd.concat(data, ignore_index=True)
