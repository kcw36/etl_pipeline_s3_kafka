"""Accessing S3 with python."""

from os import environ as ENV, remove, path, mkdir
from re import fullmatch
from csv import writer, reader

from dotenv import load_dotenv
from boto3 import client


def get_object_names_from_bucket(s_client: client, bucket_name: str) -> list[str]:
    """Returns a list of S3 object names."""
    objects = s_client.list_objects(Bucket=bucket_name)["Contents"]
    return [o['Key'] for o in objects]


def get_files(s_client: client, bucket_name) -> list[str]:
    """Return list of filtered files downloaded from S3 bucket."""
    files = get_object_names_from_bucket(s_client, bucket_name)

    path_to_data = get_dir_path()

    with open(f"{path_to_data}/lmnh_hist_data.csv", 'w', encoding="utf-8") as outfile:
        w = writer(outfile)
        w.writerow(['at', 'site', 'val', 'type'])
        filtered_files = []
        for f in files:
            if fullmatch(r"(lmnh_hist_data_[0-9]*\.csv)|(lmnh_exhibition_\w*.json)", f):
                filtered_files.append(f)
                s_client.download_file(
                    bucket_name, f, f'{path_to_data}/{f}')
                if f[-3:] == 'csv':
                    with open(f'{path_to_data}/{f}', 'r', encoding="utf-8") as infile:
                        r = reader(infile)
                        next(r)
                        for row in r:
                            w.writerow(row)
                    remove(f'{path_to_data}/{f}')
    return filtered_files


def get_data_from_file(row_number: int = -1) -> list[list]:
    """Return data from collatted csv for upload."""
    path_to_data = get_dir_path()

    with open(f"{path_to_data}/lmnh_hist_data.csv", 'r', encoding='utf-8') as f:
        r = reader(f)
        next(r)
        l = list(r)[:row_number]
        return l
    return None


def get_dir_path():
    """Return path to data directory if made."""
    path_to_data = None
    if path.exists("./data"):
        path_to_data = "./data"
    elif path.exists("../data"):
        path_to_data = "../data"
    if not path_to_data:
        mkdir("./data")
        path_to_data = "./data"
    return path_to_data


if __name__ == "__main__":

    load_dotenv()

    s3 = client("s3", aws_access_key_id=ENV["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    # Enter your own bucket name
    get_files(s3, 'some_bucket')

    print(get_data_from_file(5))

    s3.close()
