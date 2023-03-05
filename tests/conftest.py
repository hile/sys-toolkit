#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit test configuration for sys-toolkit
"""

from pathlib import Path

import pytest

from sys_toolkit.tests.mock import MockCalledMethod, MockRunCommandLineOutput

MOCK_DATA = Path(__file__).parent.joinpath('data')
NONEXISTING_FILE = MOCK_DATA.joinpath('6B6B31BD-3DCC-4CD4-BAD1-A0C8A823642E')

MOCK_UNEXPECTED_TOOLCHAIN = 'win32'

MOCK_HOSTNAME = 'test-host.example.com'
MOCK_HOSTNAME_SHORT = MOCK_HOSTNAME.split('.', maxsplit=1)[0]


@pytest.fixture
def mock_unsupported_win32_platform(monkeypatch):
    """
    Mock running SystemInfo on unexpected platform not supported by these tools
    """
    mock_platform = MockCalledMethod(return_value=MOCK_UNEXPECTED_TOOLCHAIN)
    mock_toolchain = MockCalledMethod(return_value=MOCK_UNEXPECTED_TOOLCHAIN)
    mock_output = MockRunCommandLineOutput(stdout=[])
    monkeypatch.setattr('sys_toolkit.system.info.detect_platform_family', mock_platform)
    monkeypatch.setattr('sys_toolkit.system.info.detect_toolchain_family', mock_toolchain)
    monkeypatch.setattr('sys_toolkit.system.info.run_command_lineoutput', mock_output)


@pytest.fixture
def mock_bsd_error_hostname_empty_output(monkeypatch):
    """
    Mock running SystemInfo with failing hostname command that returns empty string
    """
    mock_platform = MockCalledMethod(return_value='bsd')
    mock_toolchain = MockCalledMethod(return_value='bsd')
    mock_output = MockRunCommandLineOutput(stdout=[])
    monkeypatch.setattr('sys_toolkit.system.info.detect_platform_family', mock_platform)
    monkeypatch.setattr('sys_toolkit.system.info.detect_toolchain_family', mock_toolchain)
    monkeypatch.setattr('sys_toolkit.system.info.run_command_lineoutput', mock_output)


@pytest.fixture
def mock_darwin_platform(monkeypatch):
    """
    Mock running SystemInfo on MacOS Darwin
    """
    mock_platform = MockCalledMethod(return_value='darwin')
    mock_toolchain = MockCalledMethod(return_value='bsd')
    mock_output = MockRunCommandLineOutput(stdout=[MOCK_HOSTNAME_SHORT])
    monkeypatch.setattr('sys_toolkit.system.info.detect_platform_family', mock_platform)
    monkeypatch.setattr('sys_toolkit.system.info.detect_toolchain_family', mock_toolchain)
    monkeypatch.setattr('sys_toolkit.system.info.run_command_lineoutput', mock_output)


@pytest.fixture
def mock_freebsd_platform(monkeypatch):
    """
    Mock running SystemInfo on FreeBSD
    """
    mock_platform = MockCalledMethod(return_value='bsd')
    mock_toolchain = MockCalledMethod(return_value='bsd')
    mock_output = MockRunCommandLineOutput(stdout=[MOCK_HOSTNAME_SHORT])
    monkeypatch.setattr('sys_toolkit.system.info.detect_platform_family', mock_platform)
    monkeypatch.setattr('sys_toolkit.system.info.detect_toolchain_family', mock_toolchain)
    monkeypatch.setattr('sys_toolkit.system.info.run_command_lineoutput', mock_output)


@pytest.fixture
def mock_gnu_linux_platform(monkeypatch):
    """
    Mock running SystemInfo on GNU Linux
    """
    mock_platform = MockCalledMethod(return_value='linux')
    mock_toolchain = MockCalledMethod(return_value='gnu')
    mock_output = MockRunCommandLineOutput(stdout=[MOCK_HOSTNAME_SHORT])
    monkeypatch.setattr('sys_toolkit.system.info.detect_platform_family', mock_platform)
    monkeypatch.setattr('sys_toolkit.system.info.detect_toolchain_family', mock_toolchain)
    monkeypatch.setattr('sys_toolkit.system.info.run_command_lineoutput', mock_output)
