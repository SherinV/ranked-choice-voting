import pickle
from typing import List
from io import StringIO
from io import BytesIO
import boto3
import botocore
import pandas as pd
import json
import streamlit as st

@st.cache
def open_s3_connections() -> boto3.client("s3"):
    """
    :return: a client object from boto3, i.e. connection to S3
    """
    # configure for botocore client
    config = botocore.config.Config(
        read_timeout=360,
        connect_timeout=360,
        retries={"max_attempts": 10, "mode": "standard"},
    )
    client = boto3.client(
        "s3",
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        endpoint_url="https://s3.us-east-1.amazonaws.com/",
        config=config,
    )
    return client


def list_contents_of_bucket(
    s3_connection: boto3.client("s3"), bucket="rcvproject"
) -> List:
    """
    List contents of an s3 bucket
    """
    return s3_connection.list_objects(Bucket=bucket)["Contents"]

@st.cache
def download_and_load_pickled_model_from_s3(
    s3_connection: boto3.client("s3"), file_name: str, bucket="rcvproject"
):
    """
    Download pickled model from S3 and un-pickle it.
    """
    obj = s3_connection.get_object(Bucket=bucket, Key=file_name)["Body"].read()
    obj = BytesIO(obj)
    model = pickle.load(obj)
    return model


def df_to_stream(df: pd.DataFrame()) -> StringIO():
    """
    Helper function for upload_dataframe_to_s3 function
    :df: the dataframe to be transformed into file-like object
    :return: a file-like object
    """
    csv_buf = StringIO()
    df.to_csv(csv_buf, header=True, index=False)
    csv_buf.seek(0)
    return csv_buf


def upload_dataframe_to_s3(
    client: boto3.client("s3"),
    dataframe,
    dir_name: str,
    filename: str,
    bucket_name="rcvproject",
) -> None:
    """
    Upload dataframe to an S3 directory in an S3 bucket
    """
    if len(dataframe) > 0:
        client.put_object(
            Bucket=bucket_name,
            Body=df_to_stream(dataframe).getvalue(),
            Key=dir_name + "/" + filename,
        )


def upload_txt_file_to_s3(
    client: boto3.client("s3"),
    txt_file,
    dir_name: str,
    filename: str,
    bucket_name="rcvproject",
) -> None:
    """
    Upload a .txt file to S3
    """

    client.put_object(Bucket=bucket_name, Body=txt_file, Key=dir_name + "/" + filename)


def upload_model_to_s3(
    client: boto3.client("s3"),
    model,
    dir_name: str,
    filename: str,
    bucket_name="rcvproject",
) -> None:
    """
    Upload machine learning model to s3
    """
    pickled_model = pickle.dumps(model)
    client.put_object(
        Bucket=bucket_name, Body=pickled_model, Key=dir_name + "/" + filename
    )


def delete_files_from_s3(
    client: boto3.client("s3"), bucket: str, file_path: str
) -> None:
    """
    Delete files from S3
    """
    client.delete_object(Bucket=bucket, Key=file_path)


def get_list_of_files_matching_prefix(
    client: boto3.client("s3"), prefix: str, bucket="rcvproject"
) -> List:
    """
    List files in S3 bucket matching certain prefix
    """
    files = []
    for key in client.list_objects(Bucket=bucket, Prefix=prefix + "/")["Contents"]:
        files.append(key["Key"])
    return files


def download_and_load_txt_file_from_s3(
    s3_connection: boto3.client("s3"), file_name: str, bucket="rcvproject"
) -> str:
    """
    Download & read-in text file from S3
    """
    obj = s3_connection.get_object(Bucket=bucket, Key=file_name)["Body"].read()
    return obj.decode("utf-8")


def download_and_load_json_file_from_s3(
    s3_connection: boto3.client("s3"), file_name: str, bucket="rcvproject"
) -> str:
    """
    Download & read-in json file from S3
    """
    json_data = json.loads(
        s3_connection.get_object(Bucket=bucket, Key=file_name)["Body"].read()
    )
    return json_data


def download_csv_from_s3_and_load_as_df(
    s3_connection: boto3.client("s3"), file_name: str, header="yes", bucket="rcvproject"
) -> pd.DataFrame():
    """
    Download csv file from S3 & load into Pandas dataframe. You can
        load dataframe with or without a header.
    """
    obj = s3_connection.get_object(Bucket=bucket, Key=file_name)["Body"].read()
    s = str(obj, "utf-8")
    data = StringIO(s)

    if header == "yes":
        df = pd.read_csv(data)
        return df
    if header == "no":
        df = pd.read_csv(data, header=None)
        return df