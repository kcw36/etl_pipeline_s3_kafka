# pylint:skip-file
"""Tests for extract module."""

from unittest.mock import patch, mock_open
from pytest import mark, fixture, raises

from boto3 import client
from botocore.stub import Stubber

from extract import (get_data_from_file,
                     get_dir_path,
                     get_files,
                     get_object_names_from_bucket)


@fixture(name='client')
def test_client():
    """Test s3 client"""
    s3_client = client('s3')
    stubber = Stubber(s3_client)
    object_response = {
        'Contents': [
            {
                'Key': 'not_added.json'
            },
            {
                'Key': 'not_added.csv'
            },
            {
                'Key': 'lmnh_exhibition_bugs.json'
            },
            {
                'Key': 'lmnh_hist_data_12.csv'
            },
            {
                'Key': 'lmnh_hist_data_3.csv'
            },
            {
                'Key': 'lmnh_hist_data_4.csv'
            }
        ],
        'Name': 'string'
    }
    stubber.add_response(
        'list_objects', object_response, {'Bucket': "test_bucket"})
    stubber.activate()
    yield s3_client


@fixture(name='download_client')
def test_client_downloads():
    """Test client for downloading files."""
    with patch('boto3.client') as mock_client:
        mock_s3 = mock_client.return_value
        mock_s3.download_file.return_value = None
        mock_s3.list_objects.return_value = {
            'Contents': [
                {
                    'Key': 'not_added.json'
                },
                {
                    'Key': 'not_added.csv'
                },
                {
                    'Key': 'lmnh_exhibition_bugs.json'
                },
                {
                    'Key': 'lmnh_hist_data_12.csv'
                },
                {
                    'Key': 'lmnh_hist_data_3.csv'
                },
                {
                    'Key': 'lmnh_hist_data_4.csv'
                }
            ],
            'Name': 'string'
        }
        yield mock_client


@fixture(name='file_names')
def test_file_names():
    """Fixture of file names to use for testing."""
    return ['not_added.json',
            'not_added.csv', 'lmnh_exhibition_bugs.json', 'lmnh_hist_data_12.csv', 'lmnh_hist_data_3.csv', 'lmnh_hist_data_4.csv']


@fixture(name='test_csv')
def test_csv():
    """Fixture for mock csv contents."""
    return "at,site,val,type\n"+"2024-01-01,SiteA,123,TypeA\n"*10


def test_get_object_names_from_bucket(client):
    """Test get object names gets expected list of names from s3 bucket."""
    response = get_object_names_from_bucket(client, 'test_bucket')
    assert response == ['not_added.json',
                        'not_added.csv', 'lmnh_exhibition_bugs.json', 'lmnh_hist_data_12.csv', 'lmnh_hist_data_3.csv', 'lmnh_hist_data_4.csv']


def test_get_files_valid(download_client, file_names, test_csv):
    """Test get files downloads data from S3 matching string pattern."""
    with patch('extract.get_object_names_from_bucket') as call_buck:
        call_buck.return_value = file_names
        with patch('builtins.open', mock_open(read_data=test_csv)) as m_open:
            with patch('extract.remove') as mock_remove:
                print(get_files(download_client, 'test_bucket'))
                print(mock_remove.mock_calls)
                for i in [4, 3, 12]:
                    mock_remove.assert_any_call(
                        f"./data/lmnh_hist_data_{i}.csv")
            call_list = [("./data/lmnh_hist_data.csv", 'w'),
                         ("./data/lmnh_hist_data_12.csv", 'r'),
                         ("./data/lmnh_hist_data_4.csv", 'r'),
                         ("./data/lmnh_hist_data_3.csv", 'r')]
            for call in call_list:
                m_open.assert_any_call(call[0], call[1], encoding="utf-8")


@mark.parametrize("test_path", (('./data'), ('../data')))
def test_get_dir_path_valid(test_path):
    """Test get_dir_path finds the path when it is available."""
    def mock_exists(path):
        return path == test_path

    with patch('extract.path.exists') as p:
        p.side_effect = mock_exists
        actual = get_dir_path()
    assert actual == test_path


def test_get_data_from_file(test_csv):
    """Test get_data_from_file retrieves file data in expected format"""
    with patch("builtins.open", mock_open(read_data=test_csv*5)):
        actual = get_data_from_file(5)
        expected = [["2024-01-01", "SiteA", "123", "TypeA"]]*5
    assert actual == expected
