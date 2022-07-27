"""
Unit tests for sys_toolkit.clipboard.darwin module
"""
from subprocess import CalledProcessError

import pytest

from sys_toolkit.clipboard.darwin import DarwinClipboard, DarwinClipboardType
from sys_toolkit.exceptions import ClipboardError
from sys_toolkit.tests.mock import MockRun, MockException

from .test_base import TEST_TEXT


# pylint: disable=unused-argument
def test_clipboard_darwin_not_available(mock_clipboard_executables_missing):
    """
    Test case when darwin clipboard commands are not available on system path
    """
    assert not DarwinClipboard().available


# pylint: disable=unused-argument
def test_clipboard_darwin_available(mock_darwin_clipboard_executables_available):
    """
    Test case when darwin clipboard commands are not available on system path
    """
    assert DarwinClipboard().available


def test_clipboard_darwin_copy_error(monkeypatch):
    """
    Test copying text to darwin clipboard with command line error
    """
    mock_run_error = MockException(CalledProcessError, cmd='pbcopy', returncode=1)
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run_error)
    with pytest.raises(ClipboardError):
        DarwinClipboard().copy(TEST_TEXT)


def test_clipboard_darwin_paste_error(monkeypatch):
    """
    Test copying text from darwin clipboard with command line error
    """
    mock_run_error = MockException(CalledProcessError, cmd='pbpaste', returncode=1)
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run_error)
    with pytest.raises(ClipboardError):
        DarwinClipboard().paste()


def test_clipboard_darwin_properties():
    """
    Test basic properties of darwin clipboard object
    """
    obj = DarwinClipboard()
    assert isinstance(obj.board, DarwinClipboardType)
    assert obj.board == DarwinClipboardType.GENERAL


def test_clipboard_darwin_clear(monkeypatch):
    """
    Test clearing text on darwin clipboard (by setting it to empty string)
    """
    mock_run = MockRun()
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run)
    DarwinClipboard().clear()
    assert mock_run.call_count == 1
    args = mock_run.args[0]
    assert 'pbcopy' in args[0]


def test_clipboard_darwin_copy(monkeypatch):
    """
    Test copying text to darwin clipboard
    """
    mock_run = MockRun()
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run)
    DarwinClipboard().copy(TEST_TEXT)
    assert mock_run.call_count == 1
    args = mock_run.args[0]
    assert 'pbcopy' in args[0]


def test_clipboard_darwin_paste(monkeypatch):
    """
    Test copying text from darwin clipboard
    """
    mock_run = MockRun(stdout=bytes(TEST_TEXT, encoding='utf-8'))
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run)
    value = DarwinClipboard().paste()
    assert mock_run.call_count == 1
    args = mock_run.args[0]
    assert 'pbpaste' in args[0]
    assert value == TEST_TEXT
