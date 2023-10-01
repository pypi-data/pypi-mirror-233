import json
import os
import tempfile
import unittest
from unittest.mock import Mock, patch

import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_s3, mock_secretsmanager

from wvutils.aws import (
    _boto3_sessions,
    athena_retrieve_query,
    athena_stop_query,
    boto3_client_ctx,
    clear_boto3_sessions,
    download_from_s3,
    get_boto3_session,
    parse_s3_uri,
    secrets_fetch,
    upload_bytes_to_s3,
    upload_file_to_s3,
)

# @pytest.fixture(scope="function")
# def boto3_client_mock():
#     client_mock = Mock()
#     return client_mock

# @pytest.fixture(scope="function")
# def boto3_session_mock(boto3_client_mock):
#     session_mock = Mock()
#     session_mock.client.return_value = boto3_client_mock
#     return session_mock


@pytest.fixture(scope="function")
def safe_boto3_sessions():
    clear_boto3_sessions()
    assert len(_boto3_sessions) == 0, "Boto3 sessions failed to clear before test"
    yield
    clear_boto3_sessions()
    assert len(_boto3_sessions) == 0, "Boto3 sessions were not cleared"


@pytest.mark.parametrize(
    "s3_uri, expected",
    [
        ("s3://my-bucket/my-path", ("my-bucket", "my-path")),
        ("s3://my-bucket", ("my-bucket", "")),
        ("my-bucket/my-path", ("my-bucket", "my-path")),
    ],
)
def test_parse_s3_uri(s3_uri, expected):
    assert parse_s3_uri(s3_uri) == expected


class TestAWSSessions(unittest.TestCase):
    def setUp(self):
        self.region_name1 = "us-east-1"
        self.region_name2 = "us-west-2"

    def tearDown(self):
        # Clear the global sessions directly
        _boto3_sessions.clear()

    def test_get_boto3_session(self):
        # Sessions should be cached by region
        session1 = get_boto3_session(self.region_name1)
        session2 = get_boto3_session(self.region_name1)
        session3 = get_boto3_session(self.region_name2)
        # Check that the same session is returned for the same region
        self.assertIs(session1, session2)
        # Check that a different session is returned for a different region
        self.assertIsNot(session1, session3)

    def test_clear_boto3_sessions(self):
        # These sessions will persist for the duration of this method after clearing the global sessions
        session1 = get_boto3_session(self.region_name1)
        session2 = get_boto3_session(self.region_name2)
        num_sessions_cleared = clear_boto3_sessions()
        # Check that the correct number of sessions were cleared
        self.assertEqual(num_sessions_cleared, 2)
        # Any new sessions will be different from the previous ones
        session3 = get_boto3_session(self.region_name1)
        session4 = get_boto3_session(self.region_name2)
        # Check that the sessions are different before/after clearing
        self.assertIsNot(session1, session3)
        self.assertIsNot(session2, session4)


class TestAWSContextHelper(unittest.TestCase):
    def setUp(self):
        self.service_name = "s3"
        self.region_name = "us-east-1"

        self.session_mock = Mock()
        self.client_mock = Mock()
        self.session_mock.client.return_value = self.client_mock
        self.context_manager = boto3_client_ctx(self.service_name, self.region_name)

    def tearDown(self):
        clear_boto3_sessions()

    def test_boto3_resource(self):
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            with self.context_manager as client:
                self.assertIs(client, self.client_mock)

    def test_boto3_resource_will_raise_client_error(self):
        self.client_mock.do_something.side_effect = ClientError(
            {
                "Error": {
                    "Code": "InternalError",
                    "Message": "Something went wrong",
                },
                "ResponseMetadata": {
                    "RequestId": "123",
                    "HTTPStatusCode": 500,
                },
            },
            "operation_name",
        )
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            with self.assertRaises(ClientError):
                with self.context_manager as boto3_client:
                    boto3_client.do_something()

    def test_boto3_resource_will_raise_unknown_error(self):
        self.client_mock.do_something.side_effect = Exception("Some other error")
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            with self.assertRaises(Exception):
                with self.context_manager as boto3_client:
                    boto3_client.do_something()


@mock_s3
@pytest.mark.usefixtures("safe_boto3_sessions")
@pytest.mark.usefixtures("s3_params")
def test_download_from_s3(temp_file, s3_params):
    # Delete the pre-created temp file
    assert os.path.exists(temp_file.name)
    os.remove(temp_file.name)
    assert not os.path.exists(temp_file.name)

    file_content = "Hello World!".encode("utf-8")
    region_name, bucket_name, bucket_path = s3_params
    s3_client = boto3.client("s3", region_name=region_name)
    s3_client.create_bucket(Bucket=bucket_name)
    s3_client.put_object(Bucket=bucket_name, Key=bucket_path, Body=file_content)

    download_from_s3(
        temp_file.name,
        bucket_name,
        bucket_path,
        region_name,
        overwrite=False,
    )
    assert os.path.exists(temp_file.name)
    with open(temp_file.name, mode="rb") as rf:
        assert rf.read() == file_content


@mock_s3
@pytest.mark.usefixtures("safe_boto3_sessions")
@pytest.mark.usefixtures("s3_params")
def test_download_from_s3_without_overwrite_existing(temp_file, s3_params):
    # Delete the pre-created temp file
    assert os.path.exists(temp_file.name)
    os.remove(temp_file.name)
    assert not os.path.exists(temp_file.name)

    file_content = "Hello World!".encode("utf-8")
    region_name, bucket_name, bucket_path = s3_params
    s3_client = boto3.client("s3", region_name=region_name)
    s3_client.create_bucket(Bucket=bucket_name)
    s3_client.put_object(Bucket=bucket_name, Key=bucket_path, Body=file_content)

    with open(temp_file.name, mode="wb") as wbf:
        wbf.write("Some other content".encode("utf-8"))
    assert os.path.exists(temp_file.name)
    with open(temp_file.name, mode="rb") as rf:
        assert rf.read() != file_content

    with pytest.raises(FileExistsError):  # TODO: Add a match for the error message.
        download_from_s3(
            temp_file.name,
            bucket_name,
            bucket_path,
            region_name,
            overwrite=False,
        )
    assert os.path.exists(temp_file.name)
    with open(temp_file.name, mode="r") as rf:
        assert rf.read() == "Some other content"


@mock_s3
@pytest.mark.usefixtures("safe_boto3_sessions")
@pytest.mark.usefixtures("s3_params")
def test_download_from_s3_with_overwrite_existing(temp_file, s3_params):
    # Delete the pre-created temp file
    assert os.path.exists(temp_file.name)
    os.remove(temp_file.name)
    assert not os.path.exists(temp_file.name)

    file_content = "Hello World!".encode("utf-8")
    region_name, bucket_name, bucket_path = s3_params
    s3_client = boto3.client("s3", region_name=region_name)
    s3_client.create_bucket(Bucket=bucket_name)
    s3_client.put_object(Bucket=bucket_name, Key=bucket_path, Body=file_content)

    with open(temp_file.name, mode="wb") as wbf:
        wbf.write("Some other content".encode("utf-8"))
    assert os.path.exists(temp_file.name)
    with open(temp_file.name, mode="rb") as rf:
        assert rf.read() != file_content

    download_from_s3(
        temp_file.name,
        bucket_name,
        bucket_path,
        region_name,
        overwrite=True,
    )
    assert os.path.exists(temp_file.name)
    with open(temp_file.name, mode="rb") as rf:
        assert rf.read() == file_content


@mock_s3
@pytest.mark.usefixtures("safe_boto3_sessions")
@pytest.mark.usefixtures("s3_params")
def test_upload_file_to_s3_when_file_exists(temp_file, s3_params):
    # Delete the pre-created temp file
    assert os.path.exists(temp_file.name)
    os.remove(temp_file.name)
    assert not os.path.exists(temp_file.name)

    file_content = "Hello World!".encode("utf-8")
    region_name, bucket_name, bucket_path = s3_params
    s3_client = boto3.client("s3", region_name=region_name)
    s3_client.create_bucket(Bucket=bucket_name)

    with open(temp_file.name, mode="wb") as wbf:
        wbf.write(file_content)
    assert os.path.exists(temp_file.name)

    upload_file_to_s3(temp_file.name, bucket_name, bucket_path, region_name)
    actual = s3_client.get_object(Bucket=bucket_name, Key=bucket_path)["Body"].read()
    assert actual == file_content


@mock_s3
@pytest.mark.usefixtures("safe_boto3_sessions")
@pytest.mark.usefixtures("s3_params")
def test_upload_file_to_s3_when_file_does_not_exist(s3_params):
    region_name, bucket_name, bucket_path = s3_params

    with pytest.raises(FileNotFoundError):  # TODO: Add a match for the error message.
        upload_file_to_s3(
            "/tmp/nonexistent-file", bucket_name, bucket_path, region_name
        )


@mock_s3
@pytest.mark.usefixtures("safe_boto3_sessions")
@pytest.mark.usefixtures("s3_params")
def test_upload_bytes_to_s3(s3_params):
    file_content = "Hello World!".encode("utf-8")
    region_name, bucket_name, bucket_path = s3_params
    s3_client = boto3.client("s3", region_name=region_name)
    s3_client.create_bucket(Bucket=bucket_name)

    upload_bytes_to_s3(file_content, bucket_name, bucket_path, region_name)
    actual = s3_client.get_object(Bucket=bucket_name, Key=bucket_path)["Body"].read()
    assert actual == file_content


@mock_secretsmanager
class TestSecretsFetch(unittest.TestCase):
    def setUp(self) -> None:
        self.region_name = "us-east-1"
        self.secret_name = "my-secret"

    def create_secret(self, secret_name, secret_string):
        boto3.client("secretsmanager", region_name=self.region_name).create_secret(
            Name=secret_name, SecretString=secret_string
        )

    def tearDown(self) -> None:
        clear_boto3_sessions()

    def test_secrets_fetch_with_string_secret(self):
        secret_value = "my-secret-value"
        self.create_secret(self.secret_name, json.dumps(secret_value))
        self.assertEqual(
            secrets_fetch(self.secret_name, self.region_name),
            secret_value,
        )

    def test_secrets_fetch_with_dict_secret(self):
        secret_value = {"my-secret-key": "my-secret-value"}
        self.create_secret(self.secret_name, json.dumps(secret_value))
        self.assertEqual(
            secrets_fetch(self.secret_name, self.region_name),
            secret_value,
        )

    def test_secrets_fetch_with_list_secret(self):
        secret_value = ["my-secret-value-1", "my-secret-value-2"]
        self.create_secret(self.secret_name, json.dumps(secret_value))
        self.assertEqual(
            secrets_fetch(self.secret_name, self.region_name),
            secret_value,
        )

    def test_secrets_fetch_with_int_secret(self):
        secret_value = 123
        self.create_secret(self.secret_name, json.dumps(secret_value))
        self.assertEqual(
            secrets_fetch(self.secret_name, self.region_name),
            secret_value,
        )

    def test_secrets_fetch_with_float_secret(self):
        secret_value = 123.456
        self.create_secret(self.secret_name, json.dumps(secret_value))
        self.assertEqual(
            secrets_fetch(self.secret_name, self.region_name),
            secret_value,
        )

    def test_secrets_fetch_with_bool_secret(self):
        secret_value = True
        self.create_secret(self.secret_name, json.dumps(secret_value))
        self.assertEqual(
            secrets_fetch(self.secret_name, self.region_name),
            secret_value,
        )

    def test_secrets_fetch_with_none_secret(self):
        secret_value = None
        self.create_secret(self.secret_name, json.dumps(secret_value))
        self.assertEqual(
            secrets_fetch(self.secret_name, self.region_name),
            secret_value,
        )

    def test_secrets_fetch_raises_on_invalid_secret_json(self):
        self.create_secret(self.secret_name, "invalid-json")
        with self.assertRaises(ValueError):
            secrets_fetch(self.secret_name, self.region_name)

    def test_secrets_fetch_with_nonexistent_secret(self):
        # with pytest.raises(
        #     ClientError,
        #     match=r" ".join(
        #         (
        #             r"An error occurred \(ResourceNotFoundException\) when calling the GetSecretValue operation:",
        #             r"Secrets Manager can't find the specified secret\.",
        #         )
        #     ),
        # ):
        with self.assertRaises(ClientError):
            secrets_fetch(self.secret_name, self.region_name)


class TestAthenaRetrieveQuery(unittest.TestCase):
    def setUp(self):
        self.region_name = "us-east-1"
        self.database_name = "myDatabase"
        self.query_execution_id = "abc1234d-5efg-67hi-jklm-89n0op12qr34"
        self.s3_output_location = "s3://my-bucket/path/to/my/output"

        # Mock session that returns a mock client
        self.session_mock = Mock()
        self.client_mock = Mock()
        self.session_mock.client.return_value = self.client_mock

    def tearDown(self):
        clear_boto3_sessions()

    def test_query_state_queued(self):
        self.client_mock.get_query_execution.return_value = {
            "QueryExecution": {
                "QueryExecutionId": self.query_execution_id,
                "Status": {"State": "QUEUED"},
            },
        }
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            state_or_s3_uri = athena_retrieve_query(
                self.query_execution_id,
                self.database_name,
                self.region_name,
            )
        self.assertEqual(state_or_s3_uri, "QUEUED")

    def test_query_state_running(self):
        self.client_mock.get_query_execution.return_value = {
            "QueryExecution": {
                "QueryExecutionId": self.query_execution_id,
                "Status": {"State": "RUNNING"},
            },
        }
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            state_or_s3_uri = athena_retrieve_query(
                self.query_execution_id,
                self.database_name,
                self.region_name,
            )
        self.assertEqual(state_or_s3_uri, "RUNNING")

    def test_query_state_failed(self):
        self.client_mock.get_query_execution.return_value = {
            "QueryExecution": {
                "QueryExecutionId": self.query_execution_id,
                "Status": {"State": "FAILED"},
            },
        }
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            state_or_s3_uri = athena_retrieve_query(
                self.query_execution_id,
                self.database_name,
                self.region_name,
            )
        self.assertEqual(state_or_s3_uri, "FAILED")

    def test_query_state_succeeded(self):
        self.client_mock.get_query_execution.return_value = {
            "QueryExecution": {
                "QueryExecutionId": self.query_execution_id,
                "Status": {"State": "SUCCEEDED"},
                "ResultConfiguration": {
                    "OutputLocation": self.s3_output_location,
                },
            },
        }
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            state_or_s3_uri = athena_retrieve_query(
                self.query_execution_id,
                self.database_name,
                self.region_name,
            )
        self.assertEqual(state_or_s3_uri, self.s3_output_location)

    def test_query_state_unexpected_value(self):
        self.client_mock.get_query_execution.return_value = {
            "QueryExecution": {
                "QueryExecutionId": self.query_execution_id,
                "Status": {"State": "SOMETHING ELSE"},
            },
        }
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            with self.assertRaises(ValueError):
                athena_retrieve_query(
                    self.query_execution_id,
                    self.database_name,
                    self.region_name,
                )

    def test_query_state_unexpected_type_of_None(self):
        self.client_mock.get_query_execution.return_value = {
            "QueryExecution": {
                "QueryExecutionId": self.query_execution_id,
                "Status": {"State": None},
            },
        }
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            with self.assertRaises(ValueError):
                athena_retrieve_query(
                    self.query_execution_id,
                    self.database_name,
                    self.region_name,
                )

    def test_query_state_unexpected_type_of_int(self):
        self.client_mock.get_query_execution.return_value = {
            "QueryExecution": {
                "QueryExecutionId": self.query_execution_id,
                "Status": {"State": 1},
            },
        }
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            with self.assertRaises(ValueError):
                athena_retrieve_query(
                    self.query_execution_id,
                    self.database_name,
                    self.region_name,
                )

    def test_query_state_unexpected_type_of_float(self):
        self.client_mock.get_query_execution.return_value = {
            "QueryExecution": {
                "QueryExecutionId": self.query_execution_id,
                "Status": {"State": 1.1},
            },
        }
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            with self.assertRaises(ValueError):
                athena_retrieve_query(
                    self.query_execution_id,
                    self.database_name,
                    self.region_name,
                )

    def test_query_state_missing(self):
        self.client_mock.get_query_execution.return_value = {
            "QueryExecution": {
                "QueryExecutionId": self.query_execution_id,
                "Status": {},
            },
        }
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            with self.assertRaises(ValueError):
                athena_retrieve_query(
                    self.query_execution_id,
                    self.database_name,
                    self.region_name,
                )


class TestAthenaStopQuery(unittest.TestCase):
    def setUp(self):
        self.region_name = "us-east-1"
        self.query_execution_id = "abc1234d-5efg-67hi-jklm-89n0op12qr34"
        self.session_mock = Mock()
        self.client_mock = Mock()
        self.session_mock.client.return_value = self.client_mock

    def tearDown(self):
        clear_boto3_sessions()

    def test_stop_query(self):
        with patch("wvutils.aws.Session", return_value=self.session_mock):
            athena_stop_query(self.query_execution_id, self.region_name)
        self.client_mock.stop_query_execution.assert_called_once_with(
            QueryExecutionId=self.query_execution_id
        )
