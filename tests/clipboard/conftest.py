"""
Python test fixtures for sys_toolkit.clipboard module
"""
import pytest

from sys_toolkit.path import Executables


@pytest.fixture
def mock_darwin_clipboard_executables_missing():
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
