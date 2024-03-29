#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for sys_toolkit.encoders functions
"""
import json

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from sys_toolkit.encoders import DateTimeEncoder, format_timedelta, yaml_dump

TEST_TIMEZONE = 'UTC'
TEST_DATE = datetime(
    year=2020, month=1, day=2, hour=1, minute=2, second=3,
    tzinfo=ZoneInfo(TEST_TIMEZONE),
)

TEST_DICT = {
    'a': 1,
    'b': [1, 2, 3]
}
YAML_DUMP_RESULT = """---
a: 1
b:
  - 1
  - 2
  - 3
"""

TIMEDELTA_VALID = (
    {
        'values': ['0', 0, 0.0, timedelta(seconds=0)],
        'output': '+00:00:00',
    },
)
TIMEDELTA_INVALID = (
    None,
    [],
    'invalid'
)


def test_encoders_error() -> None:
    """
    Test encoding value which is not supported
    """
    testdata = {'string': b'string value'}
    with pytest.raises(TypeError):
        json.dumps(testdata, cls=DateTimeEncoder)


def test_format_timedelta_valid() -> None:
    """
    Test format_timedelta with various valid values
    """
    for testcase in TIMEDELTA_VALID:
        for value in testcase['values']:
            prefixed = testcase['output']
            noprefix = testcase['output'].lstrip('+-')
            assert format_timedelta(value) == prefixed
            assert format_timedelta(value, with_prefix=False) == noprefix


def test_format_timedelta_negative() -> None:
    """
    Test parsing negative time delta values
    """
    testcase = timedelta(seconds=-3623)
    expected = '-01:00:23'
    with pytest.raises(ValueError):
        format_timedelta(testcase, with_prefix=False)
    assert format_timedelta(testcase) == expected


def test_format_timedelta_errors() -> None:
    """
    Test format_timedelta with various invalid values
    """
    for testcase in TIMEDELTA_VALID:
        with pytest.raises(ValueError):
            format_timedelta(testcase)


def test_encoders_datetime_naive() -> None:
    """
    Test encoding naive datetime
    """
    testdata = {'datetime': TEST_DATE}
    expected = f'{{"datetime": "{TEST_DATE.isoformat()}"}}'
    value = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(value, str)
    assert value == expected


def test_encoders_datetime_with_timezone() -> None:
    """
    Test encoding datetime with different timezone values
    """
    testdata = {'datetime': TEST_DATE.astimezone(ZoneInfo('Europe/Helsinki'))}
    expected = f'{{"datetime": "{TEST_DATE.isoformat()}"}}'
    result = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(result, str)
    assert result == expected

    testdata = {'datetime': TEST_DATE.astimezone(ZoneInfo('US/Eastern'))}
    result = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(result, str)
    assert result == expected


def test_encoders_datetime_date() -> None:
    """
    Test encoding date value
    """
    testdata = {'date': TEST_DATE.date()}
    value = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(value, str)
    assert value == '{"date": "2020-01-02"}'


def test_encoders_datetime_time() -> None:
    """
    Test encoding time value
    """
    testdata = {'time': TEST_DATE.time()}
    value = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(value, str)
    assert value == '{"time": "01:02:03"}'


def test_encoders_datetime_timedelta() -> None:
    """
    Test encoding timedelta
    """
    testdata = {'delta': timedelta(hours=10)}
    value = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(value, str)
    assert value == '{"delta": "10:00:00"}'


def test_encoders_yaml_dump() -> None:
    """
    Test yaml_dump method returns expected document
    """
    assert yaml_dump(TEST_DICT) == YAML_DUMP_RESULT
