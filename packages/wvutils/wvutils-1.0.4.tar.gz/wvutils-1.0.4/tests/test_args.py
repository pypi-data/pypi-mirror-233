import pytest

from wvutils.args import nonempty_string, safechars_string


@pytest.mark.parametrize(
    "value, expected",
    [("a", "a"), (" a ", "a"), ("   a   ", "a")],
)
def test_nonempty_string_returns_on_nonempty_string(value, expected):
    assert nonempty_string("func_name")(value) == expected


@pytest.mark.parametrize(
    "value",
    ["", " ", "   ", "\n", "\n\n\n", "\t", "\t\t\t"],
)
def test_empty_string_raises_on_empty_string(value):
    with pytest.raises(ValueError, match=r"Must not be an empty string"):
        nonempty_string("func_name")(value)


@pytest.mark.parametrize(
    "allowed_chars,value, expected",
    [
        (None, "a", "a"),
        ("abc", "a", "a"),
        ({"a", "b", "c"}, "a", "a"),
        (("a", "b", "c"), "a", "a"),
        (["a", "b", "c"], "a", "a"),
    ],
)
def test_safechars_string_returns_on_valid_chars(allowed_chars, value, expected):
    assert safechars_string("func_name", allowed_chars=allowed_chars)(value) == expected


@pytest.mark.parametrize(
    "allowed_chars, value",
    [
        (None, "$"),
        ("abc", "d"),
        ({"a", "b", "c"}, "d"),
        (("a", "b", "c"), "d"),
        (["a", "b", "c"], "d"),
    ],
)
def test_safechars_string_raises_on_invalid_chars(allowed_chars, value):
    with pytest.raises(ValueError, match=r"Must consist of characters \[.+\]"):
        safechars_string("func_name", allowed_chars=allowed_chars)(value)


@pytest.mark.parametrize(
    "allowed_chars",
    [str(), set(), tuple(), list()],
)
def test_safechars_string_raises_on_zero_allowed_chars(allowed_chars):
    with pytest.raises(ValueError, match=r"Must provide at least one character"):
        safechars_string("func_name", allowed_chars=allowed_chars)
