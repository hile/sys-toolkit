#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for sys_toolkit.system.info module
"""
import pytest

from sys_toolkit.system.info import SystemInfo

from ..conftest import MOCK_HOSTNAME_SHORT

SYSTEM_INFO_PROPERTIES = (
    'platform_fomily',
    'toolchain_family',
    'hostname'
)
ENVIRONMENTS = {
    'gnu_linux': {
        'platform': 'linux',
        'toolchain': 'gnu'
    },
    'freebsd': {
        'platform': 'bsd',
        'toolchain': 'bsd'
    },
    'macos_darwin': {
        'platform': 'darwin',
        'toolchain': 'bsd'
    },
}


def validate_environment(obj: SystemInfo, environment: dict) -> None:
    """
    Validate SystemInfo environment
    """
    assert obj.hostname == MOCK_HOSTNAME_SHORT
    assert obj.platform_family == environment['platform']
    assert obj.toolchain_family == environment['toolchain']

    # Get values twice to trigger refresh case
    assert obj.hostname == MOCK_HOSTNAME_SHORT
    assert obj.platform_family == obj.platform_family
    assert obj.toolchain_family == obj.toolchain_family


def test_system_info_object_attributes() -> None:
    """
    Test attributes of uninitialized SystemInfo object
    """
    obj = SystemInfo()
    for attr in SYSTEM_INFO_PROPERTIES:
        assert getattr(obj, f'__{attr}__') is None


# pylint: disable=unused-argument
def test_system_info_object_darwin_unknown(
        mock_unsupported_win32_platform) -> None:
    """
    Test SystemInfo object with known OS platform and toolchain
    """
    obj = SystemInfo()
    assert obj.hostname is None


# pylint: disable=unused-argument
def test_system_info_object_darwin_macos_hostname_command_error(
        mock_bsd_error_hostname_empty_output) -> None:
    """
    Test SystemInfo object with darwin macos platform and BSD toolchain, but error
    running hostname command that returns empty string
    """
    obj = SystemInfo()
    with pytest.raises(ValueError):
        # pylint: disable=pointless-statement
        obj.hostname


# pylint: disable=unused-argument
def test_system_info_object_darwin_macos(mock_darwin_platform) -> None:
    """
    Test SystemInfo object with darwin macos platform and BSD toolchain
    """
    obj = SystemInfo()
    validate_environment(obj, ENVIRONMENTS['macos_darwin'])


# pylint: disable=unused-argument
def test_system_info_object_freebsd(mock_freebsd_platform) -> None:
    """
    Test SystemInfo object with FreeBSD platform and BSD toolchain
    """
    obj = SystemInfo()
    validate_environment(obj, ENVIRONMENTS['freebsd'])


# pylint: disable=unused-argument
def test_system_info_object_linux_gnu(mock_gnu_linux_platform) -> None:
    """
    Test SystemInfo object with linux platform and GNU toolchain
    """
    obj = SystemInfo()
    validate_environment(obj, ENVIRONMENTS['gnu_linux'])
