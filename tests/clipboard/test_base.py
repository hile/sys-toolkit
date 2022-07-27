"""
Unit tests for sys_toolkit.clipboard.base module
"""
import pytest

from sys_toolkit.clipboard.base import ClipboardBaseClass
from sys_toolkit.exceptions import ClipboardError
from sys_toolkit.tests.mock import MockRun


PASS_LINE = 'testpass123'
MIDDLE_LINE = 'Another line'
FINAL_LINE = 'Final line'
TEST_TEXT = '\n'.join([PASS_LINE, MIDDLE_LINE, FINAL_LINE])


def test_clipboard_base_class_properties():
    """
    Test properties of clipboard base class
    """
    obj = ClipboardBaseClass()
    assert obj.available is False

    assert obj.__check_required_modules__() is True
    assert obj.__check_required_env__() is True
    assert obj.__check_required_cli_commands__() is False

    with pytest.raises(NotImplementedError):
        obj.copy(TEST_TEXT)
    with pytest.raises(NotImplementedError):
        obj.paste()


def test_clipboard_base_class_paste_error_handler():
    """
    Test clipboard base class error handling for paste errors with mocked response
    """
    response = MockRun()
    obj = ClipboardBaseClass()
    with pytest.raises(ClipboardError):
        obj.__process_paste_error__(response)


def test_clipboard_base_class_paste_error(monkeypatch):
    """
    Test clipboard base class error handling for paste errors from subcommand
    """
    mock_run = MockRun(returncode=1)
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run)
    with pytest.raises(ClipboardError):
        ClipboardBaseClass().__paste_command_stdout__(('mock-test'))
    assert mock_run.call_count == 1


def test_clipboard_base_class_run_command_fail():
    """
    Test private method __run_command__ of base class with successful command
    """
    obj = ClipboardBaseClass()
    with pytest.raises(ClipboardError):
        obj.__run_command__('false')


def test_clipboard_base_class_run_command_success():
    """
    Test private method __run_command__ of base class with successful command
    """
    obj = ClipboardBaseClass()
    obj.__run_command__('true')
