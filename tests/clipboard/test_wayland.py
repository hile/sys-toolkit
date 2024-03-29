#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for sys_toolkit.clipboard.wayland module
"""
from subprocess import CalledProcessError

import pytest

from sys_toolkit.constants import DEFAULT_ENCODING
from sys_toolkit.clipboard.wayland import WaylandClipboard, WaylandClipboardSelectionType
from sys_toolkit.exceptions import ClipboardError
from sys_toolkit.tests.mock import MockRun, MockException

from .test_base import TEST_TEXT


# pylint: disable=unused-argument
def test_clipboard_wayland_env_missing(
        mock_wayland_clipboard_executables_available,
        mock_clipboard_env_missing) -> None:
    """
    Test case when wayland clipboard env vars are not available
    """
    assert not WaylandClipboard().available


# pylint: disable=unused-argument
def test_clipboard_wayland_not_available(mock_clipboard_executables_missing) -> None:
    """
    Test case when wayland clipboard commands are not available on system path
    """
    assert not WaylandClipboard().available


# pylint: disable=unused-argument
def test_clipboard_wayland_available(mock_wayland_clipboard_executables_available) -> None:
    """
    Test case when wayland clipboard commands are not available on system path
    """
    assert WaylandClipboard().available


def test_clipboard_wayland_copy_error(monkeypatch) -> None:
    """
    Test copying text to wayland clipboard with command line error
    """
    mock_run_error = MockException(CalledProcessError, cmd='pbcopy', returncode=1)
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run_error)
    with pytest.raises(ClipboardError):
        WaylandClipboard().copy(TEST_TEXT)


def test_clipboard_wayland_paste_error(monkeypatch) -> None:
    """
    Test copying text from wayland clipboard with command line error
    """
    mock_run_error = MockException(CalledProcessError, cmd='pbpaste', returncode=1)
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run_error)
    with pytest.raises(ClipboardError):
        WaylandClipboard().paste()


def test_clipboard_wayland_properties() -> None:
    """
    Test basic properties of wayland clipboard object
    """
    obj = WaylandClipboard()
    assert isinstance(obj.selection, WaylandClipboardSelectionType)
    assert obj.selection == WaylandClipboardSelectionType.PRIMARY


def test_clipboard_wayland_clear(monkeypatch) -> None:
    """
    Test clearing wayland keyboard with 'wl-copy' command
    """
    mock_run = MockRun()
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run)
    WaylandClipboard().clear()
    assert mock_run.call_count == 1
    args = mock_run.args[0]
    assert args == (('wl-copy', '--clear'),)


def test_clipboard_wayland_copy(monkeypatch) -> None:
    """
    Test copying text to wayland clipboard
    """
    mock_run = MockRun()
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run)
    WaylandClipboard().copy(TEST_TEXT)
    assert mock_run.call_count == 1
    args = mock_run.args[0]
    command = args[0]
    assert 'wl-copy' in command


def test_clipboard_wayland_paste(monkeypatch) -> None:
    """
    Test copying text from wayland clipboard
    """
    mock_run = MockRun(stdout=bytes(TEST_TEXT, encoding=DEFAULT_ENCODING))
    monkeypatch.setattr('sys_toolkit.clipboard.base.run', mock_run)
    value = WaylandClipboard().paste()
    assert mock_run.call_count == 1
    args = mock_run.args[0]
    command = args[0]
    assert 'wl-paste' in command
    assert value == TEST_TEXT
