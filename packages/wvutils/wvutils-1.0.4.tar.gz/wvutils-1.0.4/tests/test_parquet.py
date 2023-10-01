import copy
import io
import os
import uuid

import boto3
import pandas as pd
import pyarrow as pa
import pytest

# import s3fs
# from fsspec.implementations.arrow import ArrowFSWrapper
from moto import mock_s3
from pytz import utc

from wvutils.parquet import (
    _parquet_sessions,
    clear_parquet_sessions,
    create_pa_schema,
    export_dataset,
    force_dataframe_dtypes,
    get_parquet_session,
)

BASE_TEMPLATE: dict[str, str] = {
    "key_a": "string",
    "key_b": "integer",
    "key_c": "float",
    "key_d": "bool",
    "key_e": "timestamp[s]",
    "key_f": "timestamp[ms]",
    "key_g": "timestamp[ns]",
    "key_h": "string",
    "key_i": "integer",
}


@pytest.fixture(scope="function")
def primary_template():
    return copy.deepcopy(BASE_TEMPLATE)


@pytest.fixture(scope="function")
def safe_parquet_sessions():
    clear_parquet_sessions()
    assert len(_parquet_sessions) == 0, "Parquet sessions failed to clear before test"
    yield
    clear_parquet_sessions()
    assert len(_parquet_sessions) == 0, "Parquet sessions were not cleared"


BASE_DATA: dict[str, list] = {
    "key_a": ["a", "b", "c", "d", "e", "f"],
    "key_b": [1, 2, 3, 4, 5, 6],
    "key_c": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
    "key_d": [True, False, True, False, True, False],
    "key_e": (
        pd.date_range("2021-01-01", "2021-01-06", tz=utc).astype("int64") // 10**9
    )
    .astype("int64")
    .tolist(),
    "key_f": (
        pd.date_range("2021-01-07", "2021-01-12", tz=utc).astype("int64") // 10**6
    )
    .astype("int64")
    .tolist(),
    "key_g": pd.date_range("2021-01-13", "2021-01-18", tz=utc).astype("int64").tolist(),
    "key_h": ["foo", "bar", "baz", "foo", "bar", "baz"],
    "key_i": [1, 2, 3, 3, 2, 1],
}


def test_create_pa_schema():
    template = {
        "key_a": "string",
        "key_b": "integer",
        "key_c": "float",
        "key_d": "bool",
        "key_e": "timestamp[s]",
        "key_f": "timestamp[ms]",
        "key_g": "timestamp[ns]",
    }
    expected = pa.schema(
        [
            ("key_a", pa.string()),
            ("key_b", pa.int64()),
            ("key_c", pa.float64()),
            ("key_d", pa.bool_()),
            ("key_e", pa.timestamp("s", tz=utc)),
            ("key_f", pa.timestamp("ms", tz=utc)),
            ("key_g", pa.timestamp("ns", tz=utc)),
        ]
    )
    actual = create_pa_schema(template)
    assert actual == expected


def test_create_pa_schema_raises_on_invalid_type_name():
    template = {"key_a": "invalid"}
    with pytest.raises(ValueError, match=r"Unknown type name: 'invalid'"):
        create_pa_schema(template)


def test_force_dataframe_dtypes():
    template = {
        "key_a": "string",
        "key_b": "integer",
        "key_c": "float",
        "key_d": "bool",
        "key_e": "timestamp[s]",
        "key_f": "timestamp[ms]",
        "key_g": "timestamp[ns]",
    }
    df = pd.DataFrame(
        {
            "key_a": ["a", "b", "c"],
            "key_b": [1, 2, 3],
            "key_c": [1.0, 2.0, 3.0],
            "key_d": [True, False, True],
            "key_e": [
                pd.Timestamp("2021-01-01", tz=utc).value // 10**9,
                pd.Timestamp("2021-01-02", tz=utc).value // 10**9,
                pd.Timestamp("2021-01-03", tz=utc).value // 10**9,
            ],
            "key_f": [
                pd.Timestamp("2021-01-01", tz=utc).value // 10**6,
                pd.Timestamp("2021-01-02", tz=utc).value // 10**6,
                pd.Timestamp("2021-01-03", tz=utc).value // 10**6,
            ],
            "key_g": [
                pd.Timestamp("2021-01-01", tz=utc).value,
                pd.Timestamp("2021-01-02", tz=utc).value,
                pd.Timestamp("2021-01-03", tz=utc).value,
            ],
        },
        dtype="object",
    )
    expected = df.copy()
    expected = expected.astype(
        {
            "key_a": str,
            "key_b": int,
            "key_c": float,
            "key_d": bool,
        }
    )
    expected["key_e"] = pd.to_datetime(expected["key_e"], unit="s", utc=True)
    expected["key_f"] = pd.to_datetime(expected["key_f"], unit="ms", utc=True)
    expected["key_g"] = pd.to_datetime(expected["key_g"], unit="ns", utc=True)
    actual = force_dataframe_dtypes(df, template)
    pd.testing.assert_frame_equal(actual, expected)


def test_force_dataframe_dtypes_raises_on_invalid_type_name():
    template = {"key_a": "invalid"}
    df = pd.DataFrame({"key_a": ["a", "b", "c"]}).astype(str)
    with pytest.raises(ValueError, match=r"Unknown type name: 'invalid'"):
        force_dataframe_dtypes(df, template)


# TODO: Store by region name and test various regions. Might need region name to be required.


@mock_s3
@pytest.mark.usefixtures("safe_parquet_sessions")
def test_get_parquet_session():
    # Sessions should be cached by `use_s3`
    local_fs1 = get_parquet_session(use_s3=False)
    local_fs2 = get_parquet_session(use_s3=False)
    assert local_fs1 is local_fs2
    s3_fs1 = get_parquet_session(use_s3=True)
    s3_fs2 = get_parquet_session(use_s3=True)
    assert s3_fs1 is s3_fs2
    # Check that a different session is returned for a different `use_s3` value
    assert (local_fs1 is not s3_fs1) and (local_fs1 is not s3_fs2)
    assert (local_fs2 is not s3_fs1) and (local_fs2 is not s3_fs2)


@mock_s3
@pytest.mark.usefixtures("safe_parquet_sessions")
def test_clear_parquet_sessions():
    _parquet_sessions.clear()
    assert len(_parquet_sessions) == 0
    assert clear_parquet_sessions() == 0

    # Sessions should be cached by `use_s3`
    s3_fs = get_parquet_session(use_s3=True)
    local_fs = get_parquet_session(use_s3=False)
    assert len(_parquet_sessions) == 2
    assert clear_parquet_sessions() == 2

    s3_fs2 = get_parquet_session(use_s3=True)
    local_fs2 = get_parquet_session(use_s3=False)
    # New s3 sessions, although not in the cache, will be the same instances
    assert s3_fs is s3_fs2
    # New local sessions will be new instances.
    assert local_fs is not local_fs2

    # Session should still be cached by `use_s3`, even after clearing
    del s3_fs, s3_fs2, local_fs, local_fs2
    assert len(_parquet_sessions) == 2
    assert clear_parquet_sessions() == 2


@mock_s3
@pytest.mark.usefixtures("safe_parquet_sessions")
@pytest.mark.usefixtures("s3_params")
@pytest.mark.parametrize(
    "partitions_template",
    [
        {"key_h": "string", "key_i": "integer"},
        {"key_h": "string"},
        {"key_i": "integer"},
        {},
    ],
)
@pytest.mark.parametrize("basename_template", ["test-filename-{i}.parquet", None])
def test_export_dataset_s3(
    s3_params,
    partitions_template,
    basename_template,
):
    aws_access_key_id = "123"
    aws_secret_access_key = "abc"
    region_name, bucket_name, bucket_path = s3_params

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )
    s3_client = session.client("s3")
    s3_client.create_bucket(Bucket=bucket_name)

    orig_df = force_dataframe_dtypes(
        pd.DataFrame(BASE_DATA),
        BASE_TEMPLATE | partitions_template,
    )

    export_dataset(
        orig_df,
        bucket_name + "/" + bucket_path,
        primary_template=BASE_TEMPLATE,
        partitions_template=partitions_template,
        basename_template=basename_template,
        use_s3=True,
        region_name=region_name,
        use_threads=False,
        overwrite=False,
    )

    # Check each key combo only once
    for i in orig_df[list(partitions_template)].drop_duplicates().index:

        def _prepare_expected_dataframe(_df):
            df_copy = _df.copy()
            for key in partitions_template:
                df_copy = df_copy[df_copy[key] == orig_df[key].iloc[i]]
            df_copy = df_copy.reset_index(drop=True)
            df_copy = df_copy.drop(columns=list(partitions_template))
            # Datetime template types other than ns are read in as ms
            for col in df_copy.columns:
                if BASE_TEMPLATE[col] in ("timestamp[s]", "timestamp[ms]"):
                    df_copy[col] = df_copy[col].astype("datetime64[ms, UTC]")
            return df_copy

        expected_df = _prepare_expected_dataframe(orig_df)

        def _prepare_expected_path(partition_key):
            path_parts = []
            for partition_key in partitions_template:
                part_value = orig_df[partition_key].iloc[i]
                path_parts.append(f"{partition_key}={part_value}")
            if basename_template is not None:
                path_parts.append(basename_template.format(i=0))
            else:
                path_parts.append("part-0.parquet")
            return "/".join(
                [bucket_path.removeprefix("/").removesuffix("/"), *path_parts]
            )

        expected_path = _prepare_expected_path(partitions_template)
        resp = s3_client.get_object(Bucket=bucket_name, Key=expected_path)
        actual_df = pd.read_parquet(io.BytesIO(resp["Body"].read()), engine="pyarrow")

        pd.testing.assert_frame_equal(actual_df, expected_df)


@pytest.mark.parametrize(
    "partitions_template",
    [
        {"key_h": "string", "key_i": "integer"},
        {"key_h": "string"},
        {"key_i": "integer"},
        {},
    ],
)
@pytest.mark.parametrize("basename_template", ["test-filename-{i}.parquet", None])
def test_export_dataset_local(temp_dir, partitions_template, basename_template):
    output_dir = os.path.join(temp_dir, uuid.uuid4().hex)

    orig_df = force_dataframe_dtypes(
        pd.DataFrame(BASE_DATA),
        BASE_TEMPLATE | partitions_template,
    )
    export_dataset(
        orig_df,
        output_dir,
        primary_template=BASE_TEMPLATE,
        partitions_template=partitions_template,
        basename_template=basename_template,
        use_s3=False,
        region_name=None,
        use_threads=False,
        overwrite=False,
    )

    # Check each key combo only once
    for i in orig_df[list(partitions_template)].drop_duplicates().index:

        def _prepare_expected_dataframe(_df):
            df_copy = _df.copy()
            for key in partitions_template:
                df_copy = df_copy[df_copy[key] == orig_df[key].iloc[i]]
            df_copy = df_copy.reset_index(drop=True)
            df_copy = df_copy.drop(columns=list(partitions_template))
            # Datetime template types other than ns are read in as ms
            for col in df_copy.columns:
                if BASE_TEMPLATE[col] in ("timestamp[s]", "timestamp[ms]"):
                    df_copy[col] = df_copy[col].astype("datetime64[ms, UTC]")
            return df_copy

        expected_df = _prepare_expected_dataframe(orig_df)

        def _prepare_expected_path(partition_key):
            path_parts = []
            for partition_key in partitions_template:
                part_value = orig_df[partition_key].iloc[i]
                path_parts.append(f"{partition_key}={part_value}")
            if basename_template is not None:
                path_parts.append(basename_template.format(i=0))
            else:
                path_parts.append("part-0.parquet")
            return os.path.join(output_dir, *path_parts)

        expected_path = _prepare_expected_path(partitions_template)
        actual_df = pd.read_parquet(expected_path, engine="pyarrow")

        pd.testing.assert_frame_equal(actual_df, expected_df)
