#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for sys_toolkit.modules module
"""

from sys_toolkit.modules import check_available_imports

MISSING_MODULES_LIST = (
    'pathlib',
    'ljjsjfdbjdibifbdibfoboadfboa',
    'shutil',
)
AVAILABLE_MODULES_LIST = (
    'pathlib',
    'shutil',
)


def test_modules_check_available_imports_not_found() -> None:
    """
    Test checking for available import s with random, not found modules
    """
    assert check_available_imports(*MISSING_MODULES_LIST) is False


def test_modules_check_available_imports_found() -> None:
    """
    Test checking for available import s with random, not found modules
    """
    assert check_available_imports(*AVAILABLE_MODULES_LIST) is True
