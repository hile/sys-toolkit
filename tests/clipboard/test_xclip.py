"""
Unit tests for sys_toolkit.clipboard.xclip module
"""
from subprocess import CalledProcessError

import pytest

from sys_toolkit.clipboard.xclip import (
    XclipClipboard,
    XclipClipboardSelectionType,
    XCLIP_CLIPBOARD_EMPTY_ERROR,
)
from sys_toolkit.exceptions import ClipboardError
from sys_toolkit.tests.mock import MockRun, MockException

from .test_base import TEST_TEXT


# pylint: disable=unused-argument
def test_clipboard_xclip_env_missing(mock_xclip_clipboard_executables_available, mock_clipboard_env_missing):
    """
    Test case when xclip clipboard env vars are not available
    """
    assert not XclipClipboard().available


# pylint: disable=unused-argument
def test_clipboard_xclip_not_available(mock_clipboard_executables_missing):
    """
    Test case when xclip clipboard commands are not available on system path
    """
    assert not XclipClipboard().available


# pylint: disable=unused-argument
def test_clipboard_xclip_available(mock_xclip_clipboard_executables_available):
    """
    Test case when xclip clipboard commands are not available on system path
    """
    assert XclipClipboard().available


def test_clipboard_xclip_copy_error(monkeypatch):
    """
    Test copying text to xclip clipboard with command line error
    """
    mock_run_error = MockException(CalledProcessError, cmd='pbcopy', returncode=1)
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run_error)
    with pytest.raises(ClipboardError):
        XclipClipboard().copy(TEST_TEXT)


def test_clipboard_xclip_paste_error_unknown_code(monkeypatch):
    """
    Test copying text from xclip clipboard with command line error with unexpected error
    code. This command reuses the empty error to confirm that both empty error and code 1
    are required for 'None' response
    """
    mock_run_error_code = MockRun(stderr=XCLIP_CLIPBOARD_EMPTY_ERROR, returncode=2)
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run_error_code)
    with pytest.raises(ClipboardError):
        XclipClipboard().paste()


def test_clipboard_xclip_paste_error_unknown_state(monkeypatch):
    """
    Test copying text from xclip clipboard with command line error with known error code but
    missing the known error message, raising an exception
    """
    mock_run_error_code = MockRun(returncode=1)
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run_error_code)
    with pytest.raises(ClipboardError):
        XclipClipboard().paste()


def test_clipboard_xclip_paste_no_data(monkeypatch):
    """
    Test copying text from xclip clipboard when clipboard is empty and xclip returns
    known error string with returncode 1: this must return None without exception
    """
    mock_run_no_data = MockRun(stderr=XCLIP_CLIPBOARD_EMPTY_ERROR, returncode=1)
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run_no_data)
    assert XclipClipboard().paste() is None


def test_clipboard_xclip_properties():
    """
    Test basic properties of xclip clipboard object
    """
    obj = XclipClipboard()
    assert isinstance(obj.selection, XclipClipboardSelectionType)
    assert obj.selection == XclipClipboardSelectionType.PRIMARY


def test_clipboard_xclip_clear(monkeypatch):
    """
    Test clearing xclip keyboard with 'xsel' command
    """
    mock_run = MockRun()
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run)
    XclipClipboard().clear()
    assert mock_run.call_count == 2
    for args in mock_run.args:
        command = args[0]
        assert 'xsel' in command
        assert '-c' in args or '-bc' in args


def test_clipboard_xclip_copy(monkeypatch):
    """
    Test copying text to xclip clipboard
    """
    mock_run = MockRun()
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run)
    XclipClipboard().copy(TEST_TEXT)
    assert mock_run.call_count == 1
    args = mock_run.args[0]
    command = args[0]
    assert 'xclip' in command
    assert '-in' in command


def test_clipboard_xclip_paste(monkeypatch):
    """
    Test copying text from xclip clipboard
    """
    mock_run = MockRun(stdout=bytes(TEST_TEXT, encoding='utf-8'))
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run)
    value = XclipClipboard().paste()
    assert mock_run.call_count == 1
    args = mock_run.args[0]
    command = args[0]
    assert 'xclip' in command
    assert '-out' in command
    assert value == TEST_TEXT
