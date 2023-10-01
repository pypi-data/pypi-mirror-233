import json
import pickle
from io import BytesIO

import pandas as pd
from azure.storage.blob import BlobServiceClient


def exists(connection_string, container_name, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name, snapshot=None)

    return blob_client.exists()


def read_blob_as_stream(connection_string, container_name, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name, snapshot=None)

    download_stream = blob_client.download_blob()
    return download_stream


def read_blob_as_df(connection_string, container_name, blob_name, dtype_str=False, index_col=None, encoding='utf-8-sig'):
    download_stream = read_blob_as_stream(connection_string, container_name, blob_name)
    csv_file = download_stream.content_as_text(encoding=encoding)
    file = BytesIO(csv_file.encode())
    df = pd.read_csv(file, dtype='str' if dtype_str else None, index_col=index_col)

    return df


def read_pickle_from_blob(connection_string, container_name, blob_name):
    download_stream = read_blob_as_stream(connection_string=connection_string,
                                          container_name=container_name,
                                          blob_name=blob_name).readall()
    dictionary = pickle.loads(download_stream)
    return dictionary


def read_blob_as_json_object(connection_string, container_name, blob_name):
    download_stream = read_blob_as_stream(connection_string, container_name, blob_name).readall()
    json_data = json.loads(download_stream)

    return json_data


def save_df_to_blob(connection_string, container_name, blob_name, df, index=False):
    """
    We assume dfs is a list of dataframes
    """

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(data=df.to_csv(index=index), blob_type='BlockBlob')
    return True
