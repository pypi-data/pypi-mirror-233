import pytest
import math

import json
import hyperjson
import io
from json import JSONDecodeError


def test_loading_empty_value():
    with pytest.raises(ValueError):
        json.loads("")
    with pytest.raises(ValueError):
        hyperjson.loads("")


simple_types = ["1", "1.0", "-1", "null", '"str"', "true", "false"]


@pytest.mark.parametrize("payload", simple_types)
def test_simple_types(payload):
    assert json.loads(payload) == hyperjson.loads(payload)


def test_special_floats():
    assert math.isnan(json.loads("NaN"))
    assert math.isnan(hyperjson.loads("NaN"))
    assert math.isinf(json.loads("Infinity"))
    assert math.isinf(hyperjson.loads("Infinity"))
    assert math.isinf(json.loads("-Infinity"))
    assert math.isinf(hyperjson.loads("-Infinity"))


def test_string_map():
    payload = '{"foo": "bar"}'
    assert json.loads(payload) == hyperjson.loads(payload)


def test_array():
    payload = '["foo", "bar"]'
    assert json.loads(payload) == hyperjson.loads(payload)


def test_loading_docs_example():
    """
    See https://docs.python.org/3/library/json.html
    """
    payload = '["foo", {"bar":["baz", null, 1.0, 2]}]'
    assert json.loads(payload) == hyperjson.loads(payload)


def test_repeated_fields():
    """
    See https://docs.python.org/3/library/json.html#repeated-names-within-an-object
    """
    weird_json = '{"x": 1, "x": 2, "x": 3}'
    json.loads(weird_json) == hyperjson.loads(weird_json)


def test_invalid_extra_data():
    with pytest.raises(JSONDecodeError):
        hyperjson.loads("falsef")
