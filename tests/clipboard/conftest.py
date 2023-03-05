#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Python test fixtures for sys_toolkit.clipboard module
"""
import os
from typing import Iterator

import pytest

from sys_toolkit.path import Executables

CLIPBOARD_ENV_VARS = (
    'DISPLAY',
    'WAYLAND_DISPLAY',
)
DUMMY_DISPLAY = ':0.0'


@pytest.fixture
def mock_clipboard_executables_missing() -> None:
    """
    Mock path in Executables object to not contain pbcopy and pbpaste
    """
    Executables.__commands__ = {'sh': '/bin/sh'}
    yield Executables
    Executables.__commands__ = None


@pytest.fixture
def mock_clipboard_env_missing(monkeypatch) -> Iterator[dict]:
    """
    Mock environment variables to ensure
    """
    for var in CLIPBOARD_ENV_VARS:
        if os.environ.get(var, None):
            monkeypatch.delenv(var)
    yield os.environ.copy()


@pytest.fixture
def mock_darwin_clipboard_executables_available() -> Iterator[Executables]:
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
def mock_wayland_clipboard_executables_available(monkeypatch) -> Iterator[Executables]:
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
def mock_xclip_clipboard_executables_available(monkeypatch) -> Iterator[Executables]:
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
