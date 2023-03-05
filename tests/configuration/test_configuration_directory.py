"""
Unit tests for sys_toolkit.configuration.directory module
"""
from pathlib import Path

import pytest

from sys_toolkit.constants import DEFAULT_ENCODING
from sys_toolkit.configuration.directory import ConfigurationFileDirectory
from sys_toolkit.configuration.file import ConfigurationFile
from sys_toolkit.exceptions import ConfigurationError

MOCK_EXTENSIONS = (
    '.aaa',
    '.bbb',
    '.ccc',
)


def create_mock_files(directory) -> None:
    """
    Create mocked test files to given directotry
    """
    with Path(directory, 'test-no-extension').open('w', encoding=DEFAULT_ENCODING) as filedescriptor:
        filedescriptor.write('test\n')
    for extension in MOCK_EXTENSIONS:
        path = Path(directory).joinpath(f'test{extension}')
        print(f'create mock file: {path}')
        with path.open('w', encoding=DEFAULT_ENCODING) as filedescriptor:
            filedescriptor.write('test\n')


class MockConfigurationFileLoader(ConfigurationFile):
    """
    Mock object for testing configuration file loading
    """
    __loaded__ = False

    def load(self, path):
        self.__loaded__ = True


class MockConfigurationFileDirectory(ConfigurationFileDirectory):
    """
    Mock object for testing configuration file directory loading
    """
    __file_loader_class__ = MockConfigurationFileLoader
    __extensions__ = MOCK_EXTENSIONS


def test_configuration_file_directory_no_path() -> None:
    """
    Test basic attributes of a ConfigurationFileDirectory object when directory
    does not exist
    """
    obj = ConfigurationFileDirectory(path=None)
    assert obj.__path__ is None
    assert isinstance(obj.__repr__(), str)

    with pytest.raises(ConfigurationError):
        # pylint: disable=pointless-statement
        obj.file_loader_class

    with pytest.raises(ConfigurationError):
        obj.load('test')


def test_configuration_file_directory_empty_directory(tmpdir) -> None:
    """
    Test basic attributes of a ConfigurationFileDirectory object with empty directory
    """
    obj = ConfigurationFileDirectory(tmpdir.strpath)
    assert isinstance(obj.__path__, Path)
    assert isinstance(obj.__repr__(), str)
    assert obj.__path__.exists()


def test_configuration_file_directory_missing_directory(tmpdir) -> None:
    """
    Test basic attributes of a ConfigurationFileDirectory object with missing directory
    """
    directory = Path(tmpdir.strpath).joinpath('missing-directory')
    obj = ConfigurationFileDirectory(directory)
    assert isinstance(obj.__path__, Path)
    assert isinstance(obj.__repr__(), str)


def test_configuration_file_directory_not_a_directory() -> None:
    """
    Test basic attributes of a ConfigurationFileDirectory object with file passed as directory
    """
    with pytest.raises(ConfigurationError):
        ConfigurationFileDirectory(Path(__file__))


def test_configuration_file_directory_load(tmpdir) -> None:
    """
    Test loading mocked configuration files from test directory
    """
    create_mock_files(tmpdir.strpath)
    obj = MockConfigurationFileDirectory(tmpdir.strpath)
    assert len(obj.__files__) == len(MOCK_EXTENSIONS)
