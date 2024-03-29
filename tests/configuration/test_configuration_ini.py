#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for INI format configuration files
"""
from pathlib import Path

import pytest

from sys_toolkit.constants import DEFAULT_ENCODING
from sys_toolkit.configuration.base import ConfigurationSection
from sys_toolkit.exceptions import ConfigurationError
from sys_toolkit.configuration import IniConfiguration

from ..conftest import MOCK_DATA, NONEXISTING_FILE
from .test_configuration_sections import (
    validate_configuration_section,
    TEST_DEFAULT_DATA
)

# Ini supports only sections
TEST_DEFAULT_DATA = dict(
    (key, item)
    for key, item in TEST_DEFAULT_DATA.items()
    if isinstance(item, dict)
)

TEST_EMPTY = MOCK_DATA.joinpath('configuration/test_empty.ini')
TEST_INVALID = MOCK_DATA.joinpath('configuration/test_invalid.ini')
TEST_VALID = MOCK_DATA.joinpath('configuration/test_valid.ini')


class DefaultsPathsConfiguration(IniConfiguration):
    """
    Configuration file with valid default configurations
    """
    __default_paths__ = [TEST_VALID, NONEXISTING_FILE]


def test_configuration_ini_default_no_file() -> None:
    """
    Test loading default ini class without file
    """
    configuration = IniConfiguration()
    assert configuration.__repr__() == ''
    assert configuration.__path__ is None


def test_configuration_ini_nonexisting_file() -> None:
    """
    Test loading default ini class with nonexisting file
    """
    configuration = IniConfiguration(NONEXISTING_FILE)
    assert configuration.__repr__() == NONEXISTING_FILE.name
    assert configuration.__path__ == NONEXISTING_FILE


def test_configuration_ini_load_directory() -> None:
    """
    Test loading default ini class with directory as path
    """
    with pytest.raises(ConfigurationError):
        IniConfiguration(Path(__file__).parent)


# pylint: disable=unused-argument
def test_configuration_ini_load_inaccessible(tmpdir, mock_path_not_file) -> None:
    """
    Test loading default ini class with inaccessible file
    """
    path = Path(tmpdir).joinpath('test.ini')
    with path.open('w', encoding=DEFAULT_ENCODING) as filedescriptor:
        filedescriptor.write('[defaults]\ntest = value\n')
    with pytest.raises(ConfigurationError):
        IniConfiguration(path)


# pylint: disable=unused-argument
def test_configuration_ini_load_permission_denied(mock_permission_denied, tmpdir) -> None:
    """
    Test loading default ini class with no permissions to file
    """
    path = Path(tmpdir).joinpath('test.ini')
    with path.open('w', encoding=DEFAULT_ENCODING) as filedescriptor:
        filedescriptor.write('[defaults]\ntest = value\n')
    with pytest.raises(ConfigurationError):
        IniConfiguration(path)


def test_configuration_ini_empty_file() -> None:
    """
    Test loading empty ini file
    """
    configuration = IniConfiguration(TEST_EMPTY)
    assert isinstance(configuration, ConfigurationSection)
    assert configuration.__repr__() == TEST_EMPTY.name

    with pytest.raises(ConfigurationError):
        configuration.parse_data([])


def test_configuration_ini_invalid_file() -> None:
    """
    Test loading invalid YAML file
    """
    with pytest.raises(ConfigurationError):
        IniConfiguration(TEST_INVALID)


def test_configuration_ini_valid_file() -> None:
    """
    Test loading valid ini file
    """
    configuration = IniConfiguration(TEST_VALID)
    assert isinstance(configuration, ConfigurationSection)
    validate_configuration_section(configuration, TEST_DEFAULT_DATA)


def test_configuration_ini_default_paths() -> None:
    """
    Test loading ini configuration with default paths
    """
    configuration = DefaultsPathsConfiguration()
    validate_configuration_section(configuration, TEST_DEFAULT_DATA)

    # Reload data
    configuration.load(TEST_VALID)
