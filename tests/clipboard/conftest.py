"""
Python test fixtures for sys_toolkit.clipboard module
"""
import pytest

from sys_toolkit.path import Executables

DUMMY_DISPLAY = ':0.0'


@pytest.fixture
def mock_clipboard_executables_missing():
    """
    Mock path in Executables object to not contain pbcopy and pbpaste
    """
    Executables.__commands__ = {'sh': '/bin/sh'}
    yield Executables
    Executables.__commands__ = None


@pytest.fixture
def mock_darwin_clipboard_executables_available():
    """
    Mock path in Executables object to contain pbcopy and pbpaste
    """
    Executables.__commands__ = {
        'sh': '/bin/sh',
        'pbcopy': '/usr/bin/pbcopy',
        'pbpaste': '/usr/bin/pbpaste'
    }
    yield Executables
    Executables.__commands__ = None


@pytest.fixture
def mock_wayland_clipboard_executables_available(monkeypatch):
    """
    Mock path in Executables object to contain wl-copy and wl-paste

    Also sets a dummy value for WAYLAND_DISPLAY variable
    """
    monkeypatch.setenv('WAYLAND_DISPLAY', DUMMY_DISPLAY)
    Executables.__commands__ = {
        'sh': '/bin/sh',
        'wl-copy': '/usr/bin/wl-copy',
        'wl-paste': '/usr/bin/wl-paste',
    }
    yield Executables
    Executables.__commands__ = None


@pytest.fixture
def mock_xclip_clipboard_executables_available(monkeypatch):
    """
    Mock path in Executables object to contain wl-copy and wl-paste
    """
    monkeypatch.setenv('DISPLAY', DUMMY_DISPLAY)
    Executables.__commands__ = {
        'sh': '/bin/sh',
        'xclip': '/usr/bin/xclip',
        'xsel': '/usr/bin/xsel',
    }
    yield Executables
    Executables.__commands__ = None
