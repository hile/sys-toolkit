#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for sys_toolkit.tests.mock class
"""
from typing import Any, Dict, List
import pytest

from sys_toolkit.constants import DEFAULT_ENCODING
from sys_toolkit.tests.mock import (
    MockCalledMethod,
    MockCheckOutput,
    MockException,
    MockRunCommandLineOutput,
    MockReturnTrue,
    MockReturnFalse,
    MockReturnEmptyList,
    MockRun,
    MOCK_ERROR_MESSAGE,
)

from ..conftest import MOCK_DATA

TEST_FILE = MOCK_DATA.joinpath('linefile_sorted')
EXPECTED_LINE_COUNT = 6

TEST_RETURN_VALUE = 'test'
TEST_ERROR_VALUE = 'test error string'
TEST_ARGS = (1, 2, 3)

MOCK_BYTES_STRING = bytes(TEST_ERROR_VALUE, encoding=DEFAULT_ENCODING)
MOCK_KWARGS = {
    'demo': 'Demo arguments',
    'errortype': ValueError,
}


class MockError(Exception):
    """
    Test raising custom exception with custom argument processing
    """
    def __init__(self, *args: List[Any], **kwargs: Dict) -> None:
        super().__init__()
        self.call_args = args
        self.call_kwargs = kwargs


def test_mocks_mock_called_method_no_args() -> None:
    """
    Test the generic MockCalledMethod class with no arguments
    """
    obj = MockCalledMethod()
    assert callable(obj)
    value = obj()
    assert value is None
    assert obj.call_count == 1
    assert obj.args == [()]
    assert obj.kwargs == [{}]


def test_mocks_mock_called_method_args() -> None:
    """
    Test the generic MockCalledMethod class with list of arguments and return value
    """
    obj = MockCalledMethod(TEST_RETURN_VALUE)
    assert callable(obj)
    value = obj(*TEST_ARGS)
    assert value == TEST_RETURN_VALUE
    assert obj.call_count == 1
    assert obj.args == [TEST_ARGS]
    assert obj.kwargs == [{}]


def test_mocks_mock_called_method_kwargs() -> None:
    """
    Test the generic MockCalledMethod class with kwargs and return value
    """
    obj = MockCalledMethod(TEST_RETURN_VALUE)
    assert callable(obj)
    value = obj(testcase=TEST_ARGS)
    assert value == TEST_RETURN_VALUE
    assert obj.call_count == 1
    assert obj.args == [()]
    assert obj.kwargs == [{'testcase': TEST_ARGS}]


def test_mocks_mock_always_true() -> None:
    """
    Test method that returns always True
    """
    obj = MockReturnTrue()
    assert obj() is True
    assert obj(False) is True


def test_mocks_mock_always_false() -> None:
    """
    Test method that returns always False
    """
    obj = MockReturnFalse()
    assert obj() is False
    assert obj(False) is False


def test_mocks_mock_return_empty_list() -> None:
    """
    Test method that returns always an empty list
    """
    obj = MockReturnEmptyList()
    assert obj() == []
    assert obj(False) == []


def test_mocks_mock_check_output() -> None:
    """
    Test the MockCheckOutput output used to simulate subprocess.check_output
    """
    obj = MockCheckOutput(TEST_FILE)
    stdout = obj()
    assert isinstance(stdout, bytes)
    lines = str(stdout, encoding=DEFAULT_ENCODING).splitlines()
    assert len(lines) == EXPECTED_LINE_COUNT


def test_mocks_mock_run_command_line_ouptut() -> None:
    """
    Test the MockRunCommandLineOutput output
    """
    obj = MockRunCommandLineOutput(TEST_FILE)
    stdout, stderr = obj()
    assert isinstance(stdout, list)
    assert isinstance(stderr, str)
    assert len(stdout) == EXPECTED_LINE_COUNT


def test_mocks_mock_run_bytes_args() -> None:
    """
    Test the MockRun output method with bytes as arguments for stdout and stderr
    """
    obj = MockRun(stdout=MOCK_BYTES_STRING, stderr=MOCK_BYTES_STRING, returncode=2)
    value = obj()
    assert value.returncode == 2
    assert value.stdout == MOCK_BYTES_STRING
    assert value.stderr == MOCK_BYTES_STRING


def test_mocks_mock_run() -> None:
    """
    Test the MockRun output method
    """
    obj = MockRun(stdout=TEST_RETURN_VALUE, stderr=TEST_ERROR_VALUE, returncode=1)
    value = obj()
    assert value.stdout == bytes(TEST_RETURN_VALUE, encoding=DEFAULT_ENCODING)
    assert value.stderr == bytes(TEST_ERROR_VALUE, encoding=DEFAULT_ENCODING)
    assert value.returncode == 1


def test_tests_mock_called_method_no_args() -> None:
    """
    Test initializing and calling MockCalledMethod with no arguments
    """
    mock_method = MockCalledMethod()
    value = mock_method()
    assert value is None
    assert mock_method.call_count == 1
    assert mock_method.args == [()]
    assert mock_method.kwargs == [{}]

    mock_method()
    assert mock_method.call_count == 2
    assert mock_method.args == [(), ()]
    assert mock_method.kwargs == [{}, {}]


def test_tests_mock_called_method_args_and_value() -> None:
    """
    Test using MockCalledMethod to mock calls
    """
    mock_method = MockCalledMethod(return_value=MOCK_ERROR_MESSAGE)
    value = mock_method()
    assert value == MOCK_ERROR_MESSAGE
    assert mock_method.call_count == 1
    assert mock_method.args == [()]
    assert mock_method.kwargs == [{}]

    value = mock_method(MOCK_ERROR_MESSAGE)
    assert value == MOCK_ERROR_MESSAGE
    assert mock_method.call_count == 2
    assert mock_method.args == [(), (MOCK_ERROR_MESSAGE,)]
    assert mock_method.kwargs == [{}, {}]

    value = mock_method(called=mock_method)
    assert value == MOCK_ERROR_MESSAGE
    assert mock_method.call_count == 3
    assert mock_method.args == [(), (MOCK_ERROR_MESSAGE,), ()]
    assert mock_method.kwargs == [{}, {}, {'called': mock_method}]


def test_tests_mock_exception_no_args() -> None:
    """
    Mock raising generic exception without specifying any arguments
    """
    mock_error = MockException()
    with pytest.raises(Exception) as raised_error:
        mock_error()
    assert mock_error.call_count == 1
    assert mock_error.args == [()]
    assert mock_error.kwargs == [{}]
    # pylint: disable=protected-access
    exception = raised_error._excinfo[1]
    assert str(exception) == MOCK_ERROR_MESSAGE


def test_tests_mock_check_output() -> None:
    """
    Test utility callback to mock subprocess.check_output. Look for this known
    line (this function's signature) from output
    """
    mock_check_output = MockCheckOutput(__file__)
    stdout = mock_check_output()
    assert mock_check_output.call_count == 1
    assert isinstance(stdout, bytes)

    line = 'def test_tests_mock_check_output() -> None:'
    assert line in str(stdout, DEFAULT_ENCODING).splitlines()


def test_tests_mock_exception_no_args_no_default_message() -> None:
    """
    Mock raising generic exception without default error message
    """
    mock_error = MockException(default_message=False)
    with pytest.raises(Exception) as raised_error:
        mock_error()
    assert mock_error.call_count == 1
    assert mock_error.args == [()]
    assert mock_error.kwargs == [{}]
    # pylint: disable=protected-access
    exception = raised_error._excinfo[1]
    assert str(exception) != MOCK_ERROR_MESSAGE


def test_tests_mock_exception_value_error() -> None:
    """
    Mock raising ValueError without specifying any arguments
    """
    mock_error = MockException(exception=ValueError)
    with pytest.raises(ValueError) as raised_error:
        mock_error()
    assert mock_error.call_count == 1
    assert mock_error.args == [()]
    assert mock_error.kwargs == [{}]
    # pylint: disable=protected-access
    exception = raised_error._excinfo[1]
    assert isinstance(exception, ValueError)
    assert str(exception) == MOCK_ERROR_MESSAGE


def test_tests_mock_exception_custom_error_args() -> None:
    """
    Mock raising custom exception with specific arguments
    """
    mock_error = MockException(
        exception=MockError,
        exception_kwargs=MOCK_KWARGS,
    )
    arg = 'argumentative'
    kwargs = {
        'errors': 'yes we like errors'
    }
    with pytest.raises(MockError) as raised_error:
        mock_error(arg, **kwargs)
    assert mock_error.call_count == 1
    assert mock_error.args == [(arg,)]
    assert mock_error.kwargs == [kwargs]
    # pylint: disable=protected-access
    exception = raised_error._excinfo[1]
    assert isinstance(exception, MockError)
    assert str(exception) == ''


def test_tests_mock_return_method_values_true() -> None:
    """
    Unit test for mock method that always returns True
    """
    limit = 2
    method = MockReturnTrue()
    for _i in range(0, limit):
        assert method() is True
    assert method.call_count == limit


def test_tests_mock_return_method_values_false() -> None:
    """
    Unit test for mock method that always returns False
    """
    limit = 2
    method = MockReturnFalse()
    for _i in range(0, limit):
        assert method() is False
    assert method.call_count == limit


def test_tests_mock_return_method_values_empty_list() -> None:
    """
    Unit test for mock method that always returns empty list
    """
    limit = 2
    method = MockReturnEmptyList()
    for _i in range(0, limit):
        assert method() == []
    assert method.call_count == limit
