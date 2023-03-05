"""
Unit tests for yaml format configuration files
"""
from pathlib import Path

import pytest

from sys_toolkit.constants import DEFAULT_ENCODING
from sys_toolkit.configuration.base import ConfigurationSection
from sys_toolkit.configuration import YamlConfiguration
from sys_toolkit.exceptions import ConfigurationError

from ..conftest import MOCK_DATA, NONEXISTING_FILE
from .test_configuration_sections import (
    validate_configuration_section,
    TEST_DEFAULT_DATA
)

TEST_CONFIGURATIONS = Path(MOCK_DATA, 'configuration')

TEST_EMPTY = TEST_CONFIGURATIONS.joinpath('test_empty.yml')
TEST_INVALID = TEST_CONFIGURATIONS.joinpath('test_invalid.yml')
TEST_VALID = TEST_CONFIGURATIONS.joinpath('test_valid.yml')


class DefaultsPathsConfiguration(YamlConfiguration):
    """
    Configuration file with valid default configurations
    """
    __default_paths__ = [TEST_VALID, NONEXISTING_FILE]


def test_configuration_yml_default_no_file() -> None:
    """
    Test loading default YAML class without file
    """
    configuration = YamlConfiguration()
    assert configuration.__repr__() == ''
    assert configuration.__path__ is None


def test_configuration_yml_empty_file() -> None:
    """
    Test loading empty YAML file
    """
    configuration = YamlConfiguration(TEST_EMPTY)
    assert isinstance(configuration, ConfigurationSection)
    assert configuration.__repr__() == TEST_EMPTY.name


def test_configuration_yml_nonexisting_file() -> None:
    """
    Test loading default YAML class with nonexisting file
    """
    configuration = YamlConfiguration(NONEXISTING_FILE)
    assert configuration.__repr__() == NONEXISTING_FILE.name
    assert configuration.__path__ == NONEXISTING_FILE


def test_configuration_yml_load_directory() -> None:
    """
    Test loading default YAML class with directory as path
    """
    with pytest.raises(ConfigurationError):
        YamlConfiguration(Path(__file__).parent)


# pylint: disable=unused-argument
def test_configuration_yml_load_inaccessible(mock_path_not_file, tmpdir) -> None:
    """
    Test loading default YAML class with inaccessible file
    """
    path = Path(tmpdir).joinpath('test.yml')
    with path.open('w', encoding=DEFAULT_ENCODING) as filedescriptor:
        filedescriptor.write('---\n')

    with pytest.raises(ConfigurationError):
        YamlConfiguration(path)


# pylint: disable=unused-argument
def test_configuration_yml_load_permission_denied(mock_permission_denied, tmpdir) -> None:
    """
    Test loading default YAML class with no permissions to file
    """
    path = Path(tmpdir).joinpath('test.yml')
    with path.open('w', encoding=DEFAULT_ENCODING) as filedescriptor:
        filedescriptor.write('---\n')

    with pytest.raises(ConfigurationError):
        YamlConfiguration(path)


def test_configuration_yml_invalid_file() -> None:
    """
    Test loading invalid YAML file
    """
    with pytest.raises(ConfigurationError):
        YamlConfiguration(TEST_INVALID)


def test_configuration_yml_valid_file() -> None:
    """
    Test loading valid YAML file
    """
    configuration = YamlConfiguration(TEST_VALID)
    assert isinstance(configuration, ConfigurationSection)
    validate_configuration_section(configuration, TEST_DEFAULT_DATA)


def test_configuration_yml_default_paths() -> None:
    """
    Test loading YAML configuration with default paths
    """
    configuration = DefaultsPathsConfiguration()
    validate_configuration_section(configuration, TEST_DEFAULT_DATA)
