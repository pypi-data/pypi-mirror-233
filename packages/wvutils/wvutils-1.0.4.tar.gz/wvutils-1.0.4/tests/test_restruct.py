from collections import deque
from unittest import mock

import cloudpickle
import pytest
import rapidjson

from wvutils.errors import (
    HashEncodeError,
    HashError,
    JSONDecodeError,
    JSONEncodeError,
    JSONError,
    PickleDecodeError,
    PickleEncodeError,
    PickleError,
)

from wvutils.restruct import (
    gen_hash,
    json_dump,
    json_dumps,
    json_load,
    json_loads,
    jsonl_dump,
    jsonl_dumps,
    jsonl_loader,
    pickle_dump,
    pickle_dumps,
    pickle_load,
    pickle_loads,
    squeegee_loader,
)

OUT_OF_RANGE_FLOAT_STRINGS = ["inf", "-inf", "nan", "-nan"]
OUT_OF_RANGE_FLOATS = list(map(float, OUT_OF_RANGE_FLOAT_STRINGS))


class Unstringable:
    def __str__(self):
        return None


class Unpicklable:
    def __getstate__(self):
        raise TypeError("Cannot pickle")

    def __setstate__(self, state):
        pass


JSON_SERIALIZE_TESTS = [
    ("test", '"test"'),
    (123, "123"),
    (1.23, "1.23"),
    (1.23 + 4.56j, '"(1.23+4.56j)"'),  # __str__ representation
    (False, "false"),
    (True, "true"),
    (set(), '"set()"'),  # __str__ representation
    ({0, 1, 2}, '"{0, 1, 2}"'),  # __str__ representation
    (tuple(), "[]"),  # list representation
    ((1, 2, 3), "[1,2,3]"),  # list representation
    ([], "[]"),
    ([1, 2, 3], "[1,2,3]"),
    ({}, "{}"),
    ({"a": 1, "b": 2}, '{"a":1,"b":2}'),
    ({1: "a", 2: "b"}, "\"{1: 'a', 2: 'b'}\""),
    ({1.0: "a", 2.0: "b"}, "\"{1.0: 'a', 2.0: 'b'}\""),
    (None, "null"),
    (b"test", '"test"'),  # __str__ representation
    (bytearray(b"test"), '"test"'),  # __str__ representation
]


@pytest.mark.parametrize("value, expected", JSON_SERIALIZE_TESTS)
def test_json_dumps(value, expected):
    assert json_dumps(value) == expected


@pytest.mark.parametrize("exception", [TypeError, JSONEncodeError, JSONError])
def test_json_dumps_raises_on_unserializable_type(exception):
    with pytest.raises(exception, match=r"Could not encode object"):
        json_dumps(Unstringable())


@pytest.mark.parametrize("value", OUT_OF_RANGE_FLOATS)
@pytest.mark.parametrize("exception", [TypeError, JSONEncodeError, JSONError])
def test_json_dumps_raises_on_out_of_range_floats(value, exception):
    with pytest.raises(exception, match=r"Could not encode object"):
        json_dumps(value)


@pytest.mark.parametrize("value, expected", JSON_SERIALIZE_TESTS)
def test_json_dump(temp_file, value, expected):
    json_dump(value, temp_file.name)
    temp_file.seek(0)
    assert temp_file.read().decode("utf-8") == expected


@pytest.mark.parametrize("value", OUT_OF_RANGE_FLOATS)
@pytest.mark.parametrize("exception", [TypeError, JSONEncodeError, JSONError])
def test_json_dump_raises_on_out_of_range_floats(temp_file, value, exception):
    with pytest.raises(exception, match=r"Could not encode object"):
        json_dump(value, temp_file.name)


@pytest.mark.parametrize("exception", [TypeError, JSONEncodeError, JSONError])
def test_json_dump_raises_on_unserializable_type(temp_file, exception):
    with pytest.raises(exception, match=r"Could not encode object"):
        json_dump(Unstringable(), temp_file.name)


JSON_DESERIALIZE_TESTS = [
    ('"test"', "test"),
    ("123", 123),
    ("1.23", 1.23),
    ("false", False),
    ("true", True),
    ("[]", []),
    ("[1,2,3]", [1, 2, 3]),
    ("[1, 2, 3]", [1, 2, 3]),
    ("{}", {}),
    ('{"a":1,"b":2}', {"a": 1, "b": 2}),
    ('{"a": 1, "b": 2}', {"a": 1, "b": 2}),
    (
        "\n".join(
            (
                "{",
                '    "a": 1,',
                '    "b": 2,',
                '    "c": [1, 2, 3],',
                '    "d": {"e": 4, "f": 5}',
                "}",
            )
        ),
        {"a": 1, "b": 2, "c": [1, 2, 3], "d": {"e": 4, "f": 5}},
    ),
    ("null", None),
]


@pytest.mark.parametrize("value, expected", JSON_DESERIALIZE_TESTS)
def test_json_loads(value, expected):
    assert json_loads(value) == expected


@pytest.mark.parametrize("value", OUT_OF_RANGE_FLOAT_STRINGS)
@pytest.mark.parametrize("exception", [ValueError, JSONDecodeError, JSONError])
def test_json_loads_raises_on_out_of_range_floats(value, exception):
    with pytest.raises(exception, match=r"Could not decode object"):
        json_loads(value)


@pytest.mark.parametrize("value, expected", JSON_DESERIALIZE_TESTS)
def test_json_load(temp_file, value, expected):
    temp_file.write(value.encode("utf-8"))
    temp_file.seek(0)
    assert json_load(temp_file.name) == expected


@pytest.mark.parametrize("value", OUT_OF_RANGE_FLOAT_STRINGS)
@pytest.mark.parametrize("exception", [ValueError, JSONDecodeError, JSONError])
def test_json_load_raises_on_out_of_range_floats(value, temp_file, exception):
    temp_file.write(value.encode("utf-8"))
    temp_file.seek(0)
    with pytest.raises(exception, match=r"Could not decode file '.+'"):
        json_load(temp_file.name)


JSONL_SERIALIZE_TESTS = [
    (["this", "is", "a", "test"], '"this"\n"is"\n"a"\n"test"'),
    ([1, 2, 3, 4], "1\n2\n3\n4"),
    ([1.23, 4.56, 7.89], "1.23\n4.56\n7.89"),
    ([1.23 + 4.56j, 7.89 + 1.23j], '"(1.23+4.56j)"\n"(7.89+1.23j)"'),
    ([False, True], "false\ntrue"),
    ([set(), {0, 1, 2}], '"set()"\n"{0, 1, 2}"'),
    ([tuple(), (1, 2, 3)], "[]\n[1,2,3]"),
    ([[], [1, 2, 3]], "[]\n[1,2,3]"),
    ([{}, {"a": 1, "b": 2}], '{}\n{"a":1,"b":2}'),
    (
        [{1: "a", 2: "b"}, {1.0: "a", 2.0: "b"}],
        "\"{1: 'a', 2: 'b'}\"\n\"{1.0: 'a', 2.0: 'b'}\"",
    ),
    ([None, b"test", bytearray(b"test")], 'null\n"test"\n"test"'),
    ([], ""),
]


@pytest.mark.parametrize("value, expected", JSONL_SERIALIZE_TESTS)
def test_jsonl_dumps(value, expected):
    assert jsonl_dumps(value) == expected


@pytest.mark.parametrize("value", OUT_OF_RANGE_FLOATS)
@pytest.mark.parametrize("exception", [TypeError, JSONEncodeError, JSONError])
def test_jsonl_dumps_raises_on_out_of_range_floats(value, exception):
    with pytest.raises(exception, match=r"Could not encode objects"):
        jsonl_dumps([value])


@pytest.mark.parametrize("value, expected", JSONL_SERIALIZE_TESTS)
def test_jsonl_dump(temp_file, value, expected):
    jsonl_dump(value, temp_file.name)
    temp_file.seek(0)
    assert temp_file.read().decode("utf-8") == expected


@pytest.mark.parametrize("value", OUT_OF_RANGE_FLOATS)
@pytest.mark.parametrize("exception", [TypeError, JSONEncodeError, JSONError])
def test_jsonl_dump_raises_on_out_of_range_floats(value, temp_file, exception):
    with pytest.raises(exception, match=r"Could not encode objects"):
        jsonl_dump([value], temp_file.name)


JSONL_DESERIALIZE_TESTS = [
    ('"this"\n"is"\n"a"\n"test"\n', ["this", "is", "a", "test"]),
    ("1\n2\n3\n4\n", [1, 2, 3, 4]),
    ("1.23\n4.56\n7.89\n", [1.23, 4.56, 7.89]),
    ("false\ntrue\n", [False, True]),
    ("[]\n[1,2,3]\n", [[], [1, 2, 3]]),
    ('{}\n{"a":1,"b":2}\n', [{}, {"a": 1, "b": 2}]),
    ("null\n", [None]),
    ("", []),
]


@pytest.mark.parametrize("value, expected", JSONL_DESERIALIZE_TESTS)
def test_jsonl_loader(value, expected):
    with (
        mock.patch("wvutils.restruct.resolve_path", lambda path: path),
        mock.patch("builtins.open", mock.mock_open(read_data=value)),
    ):
        assert list(jsonl_loader("nonexistent_file.json")) == expected


@pytest.mark.parametrize("value", OUT_OF_RANGE_FLOAT_STRINGS)
@pytest.mark.parametrize("exception", [ValueError, JSONDecodeError, JSONError])
def test_jsonl_loader_raises_on_out_of_range_floats(value, exception):
    with (
        mock.patch("wvutils.restruct.resolve_path", lambda path: path),
        mock.patch("builtins.open", mock.mock_open(read_data=value)),
    ):
        with pytest.raises(exception, match=r"Could not decode file '.+'"):
            list(jsonl_loader("nonexistent_file.json"))


@pytest.mark.parametrize("value", ['"test"\n\n"test"', '\n\n"test"', '"test"\n\n'])
@pytest.mark.parametrize("exception", [ValueError, JSONDecodeError, JSONError])
def test_jsonl_loader_raises_on_empty_lines(value, exception):
    with (
        mock.patch("wvutils.restruct.resolve_path", lambda path: path),
        mock.patch("builtins.open", mock.mock_open(read_data=value)),
    ):
        with pytest.raises(exception, match=r"Could not decode file '.+'"):
            list(jsonl_loader("nonexistent_file.json"))


@pytest.mark.parametrize(
    "value, expected",
    [
        # Empty lines
        ("", []),
        ("\n", []),
        ("\n\n", []),
        ("\r\n", []),
        ("\r\n\r\n", []),
        # Single values
        ('"test"', ["test"]),
        ('"test"\n', ["test"]),
        ('"test"\n"test"', ["test", "test"]),
        ('"test"\n"test"\n', ["test", "test"]),
        ('"test"\r\n', ["test"]),
        ('"test"\r\n"test"', ["test", "test"]),
        ('"test"\r\n"test"\r\n', ["test", "test"]),
        ("123", [123]),
        ("123\n", [123]),
        ("123\n456", [123, 456]),
        ("123\n456\n", [123, 456]),
        ("123\r\n", [123]),
        ("123\r\n456", [123, 456]),
        ("123\r\n456\r\n", [123, 456]),
        ("true", [True]),
        ("true\n", [True]),
        ("true\nfalse", [True, False]),
        ("true\nfalse\n", [True, False]),
        ("true\r\n", [True]),
        ("true\r\nfalse", [True, False]),
        ("true\r\nfalse\r\n", [True, False]),
        ("null", [None]),
        ("null\n", [None]),
        ("null\nnull", [None, None]),
        ("null\nnull\n", [None, None]),
        ("null\r\n", [None]),
        ("null\r\nnull", [None, None]),
        ("{}", [{}]),
        ("{}\n", [{}]),
        ("{}\n{}", [{}, {}]),
        ("{}\n{}\n", [{}, {}]),
        ("{}\r\n", [{}]),
        ("{}\r\n{}", [{}, {}]),
        ("{}\r\n{}\r\n", [{}, {}]),
        ('{"a":"b"}', [{"a": "b"}]),
        ('{"a":"b"}\n', [{"a": "b"}]),
        ('{"a":"b"}\n{"a":"b"}', [{"a": "b"}, {"a": "b"}]),
        ('{"a":"b"}\n{"a":"b"}\n', [{"a": "b"}, {"a": "b"}]),
        ('{"a":"b"}\r\n', [{"a": "b"}]),
        ('{"a":"b"}\r\n{"a":"b"}', [{"a": "b"}, {"a": "b"}]),
        ('{"a":"b"}\r\n{"a":"b"}\r\n', [{"a": "b"}, {"a": "b"}]),
        ("null\r\nnull\r\n", [None, None]),
        # Lists of objects
        ("[]", []),
        ("[]\n", []),
        ("[]\n[]", []),
        ("[]\n[]\n", []),
        ("[]\r\n", []),
        ("[]\r\n[]", []),
        ("[]\r\n[]\r\n", []),
        ("[1]", [1]),
        ("[1]\n", [1]),
        ("[1]\n[2]", [1, 2]),
        ("[1]\n[2]\n", [1, 2]),
        ("[1]\r\n", [1]),
        ("[1]\r\n[2]", [1, 2]),
        ("[1]\r\n[2]\r\n", [1, 2]),
        ("[1,2]", [1, 2]),
        ("[1,2]\n", [1, 2]),
        ("[1,2]\n[3,4]", [1, 2, 3, 4]),
        ("[1,2]\n[3,4]\n", [1, 2, 3, 4]),
        ("[1,2]\r\n", [1, 2]),
        ("[1,2]\r\n[3,4]", [1, 2, 3, 4]),
        ("[1,2]\r\n[3,4]\r\n", [1, 2, 3, 4]),
        ("[1,2,3]", [1, 2, 3]),
        ("[1,2,3]\n", [1, 2, 3]),
        ("[1,2,3]\n[4,5,6]", [1, 2, 3, 4, 5, 6]),
        ("[1,2,3]\n[4,5,6]\n", [1, 2, 3, 4, 5, 6]),
        ("[1,2,3]\r\n", [1, 2, 3]),
        ("[1,2,3]\r\n[4,5,6]", [1, 2, 3, 4, 5, 6]),
        ("[1,2,3]\r\n[4,5,6]\r\n", [1, 2, 3, 4, 5, 6]),
        ('[{"a":1},{"b":2}]', [{"a": 1}, {"b": 2}]),
        ('[{"a":1},{"b":2}]\n', [{"a": 1}, {"b": 2}]),
        (
            '[{"a":1},{"b":2}]\n[{"c":3},{"d":4}]',
            [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}],
        ),
        (
            '[{"a":1},{"b":2}]\n[{"c":3},{"d":4}]\n',
            [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}],
        ),
        ('[{"a":1},{"b":2}]\r\n', [{"a": 1}, {"b": 2}]),
        (
            '[{"a":1},{"b":2}]\r\n[{"c":3},{"d":4}]',
            [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}],
        ),
        (
            '[{"a":1},{"b":2}]\r\n[{"c":3},{"d":4}]\r\n',
            [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}],
        ),
        # Whole file is a single object
        (
            "\n".join(
                (
                    "{",
                    '    "a": 1,',
                    '    "b": 2,',
                    '    "c": [1, 2, 3],',
                    '    "d": {"e": 4, "f": 5}',
                    "}",
                )
            ),
            [{"a": 1, "b": 2, "c": [1, 2, 3], "d": {"e": 4, "f": 5}}],
        ),
        # Whole file is a list of objects
        (
            "\n".join(
                (
                    "[",
                    "    {",
                    '        "a": 1,',
                    '        "b": 2,',
                    '        "c": [1, 2, 3],',
                    '        "d": {"e": 4, "f": 5}',
                    "    },",
                    '    {"g": 6, "h": 7, "i": [4, 5, 6], "j": {"k": 8, "l": 9}},',
                    "    {",
                    '        "m": 10,',
                    '        "n": 11,',
                    '        "o": [7, 8, 9],',
                    '        "p": {"q": 12, "r": 13}',
                    "    }",
                    "]",
                )
            ),
            [
                {"a": 1, "b": 2, "c": [1, 2, 3], "d": {"e": 4, "f": 5}},
                {"g": 6, "h": 7, "i": [4, 5, 6], "j": {"k": 8, "l": 9}},
                {"m": 10, "n": 11, "o": [7, 8, 9], "p": {"q": 12, "r": 13}},
            ],
        ),
        # # Mix of compact and pretty-printed JSON
        # (
        #     "\n".join(
        #         (
        #             "{",
        #             '    "a": 1,',
        #             '    "b": 2,',
        #             '    "c": [1, 2, 3],',
        #             '    "d": {"e": 4, "f": 5}',
        #             "}",
        #             '{"a":1,"b":2,"c":[1,2,3],"d":{"e":4,"f":5}}',
        #         )
        #     ),
        #     [{"a": 1, "b": 2, "c": [1, 2, 3], "d": {"e": 4, "f": 5}}],
        # ),
    ],
)
def test_squeegee_loader(value, expected):
    with (
        mock.patch("wvutils.restruct.resolve_path", lambda path: path),
        mock.patch("builtins.open", mock.mock_open(read_data=value)),
    ):
        assert list(squeegee_loader("nonexistent_file.json")) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (b"foo", "acbd18db4cc2f85cedef654fccc4a4d8"),
        ("foo", "acbd18db4cc2f85cedef654fccc4a4d8"),
        (["foo", "bar"], "1ea13cb52ddd7c90e9f428d1df115d8f"),
        (("foo", "bar"), "1ea13cb52ddd7c90e9f428d1df115d8f"),
        (deque(["foo", "bar"]), "1ea13cb52ddd7c90e9f428d1df115d8f"),
    ],
)
def test_gen_hash(value, expected):
    assert gen_hash(value) == expected


@pytest.mark.parametrize(
    "value",
    [set(["foo", "bar"]), frozenset(["foo", "bar"]), {"foo", "bar"}],
)
@pytest.mark.parametrize("exception", [TypeError, HashEncodeError, HashError])
def test_gen_hash_raises_on_unhashable_object(value, exception):
    with pytest.raises(exception, match=r"Could not hash object"):
        gen_hash(value)


# TODO: Add tests for other types
PICKLE_SERIALIZE_TESTS = [
    b"foo",
    "foo",
    ["foo", "bar"],
    ("foo", "bar"),
    deque(["foo", "bar"]),
    set(["foo", "bar"]),
    frozenset(["foo", "bar"]),
    {"foo", "bar"},
]


# TODO: Test needs to be more thorough and test more types
@pytest.mark.parametrize("value", PICKLE_SERIALIZE_TESTS)
def test_pickle_dumps(value):
    pkl = pickle_dumps(value)
    assert cloudpickle.loads(pkl) == value


@pytest.mark.parametrize("exception", [TypeError, PickleEncodeError, PickleError])
def test_pickle_dumps_raises_on_unpicklable_object(exception):
    with pytest.raises(exception, match=r"Could not pickle object"):
        pickle_dumps(Unpicklable())


# TODO: Test needs to be more thorough and test more types
@pytest.mark.parametrize("value", PICKLE_SERIALIZE_TESTS)
def test_pickle_dump(temp_file, value):
    pickle_dump(value, temp_file.name)
    temp_file.seek(0)
    assert cloudpickle.load(temp_file) == value


@pytest.mark.parametrize("exception", [TypeError, PickleEncodeError, PickleError])
def test_pickle_dump_raises_on_unpicklable_object(temp_file, exception):
    with pytest.raises(exception, match=r"Could not pickle object"):
        pickle_dump(Unpicklable(), temp_file.name)


PICKLE_DESERIALIZE_TESTS = [
    b"foo",
    "foo",
    ["foo", "bar"],
    ("foo", "bar"),
    deque(["foo", "bar"]),
    set(["foo", "bar"]),
    frozenset(["foo", "bar"]),
    {"foo", "bar"},
]


# TODO: Test needs to be more thorough and test more types
@pytest.mark.parametrize("value", PICKLE_DESERIALIZE_TESTS)
def test_pickle_loads(value):
    assert pickle_loads(cloudpickle.dumps(value)) == value


@pytest.mark.parametrize("exception", [ValueError, PickleDecodeError, PickleError])
def test_pickle_loads_raises_on_malformed_pickle(exception):
    with pytest.raises(exception, match=r"Could not unpickle object"):
        pickle_loads(b"f00")


# TODO: Test needs to be more thorough and test more types
@pytest.mark.parametrize("value", PICKLE_DESERIALIZE_TESTS)
def test_pickle_load(temp_file, value):
    cloudpickle.dump(value, temp_file)
    temp_file.seek(0)
    assert pickle_load(temp_file.name) == value


@pytest.mark.parametrize("exception", [ValueError, PickleDecodeError, PickleError])
def test_pickle_load_raises_on_malformed_pickle(temp_file, exception):
    temp_file.write(b"f00")
    temp_file.seek(0)
    with pytest.raises(exception, match=r"Could not unpickle object"):
        pickle_load(temp_file.name)


# def test_pickle_load_raises_on_nonexistent_file():
#     with pytest.raises(FileNotFoundError, match=r".*No such file or directory: .+"):
#         pickle_load("nonexistent_file.json")
