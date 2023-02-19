"""
Unit tests for cli_toolkit.path.Executables class
"""

import os

from pathlib import Path

import pytest

from sys_toolkit.path import Executables
from sys_toolkit.tests.mock import MockException

MOCK_PATH_DIRS = (
    'bin',
    'sbin',
    'opt/bin',
)
MOCK_PATH_EXECUTABLES = (
    'bin/ls',
    'bin/sh',
    'opt/bin/sh',
)
MOCK_PATH_NON_EXECUTABLES = (
    'opt/bin/README.md',
)
MOCK_PATH_SUBDIRS = (
    'bin/.git',
    'opt/bin/unexpected',
)
MOCK_PERM_EXECUTABLE = int('0755', 8)
MOCK_PERM_NON_EXECUTABLE = int('0640', 8)

# Duplicate sh commands in path
MOCK_EXECUTABLE_COUNT_POSIX = 2
MOCK_EXECUTABLE_COUNT_WINDOWS = MOCK_EXECUTABLE_COUNT_POSIX + len(MOCK_PATH_NON_EXECUTABLES)
MOCK_COMMAND_AVAILABLE = 'sh'
MOCK_COMMAND_NOT_AVAILABLE = 'jvodsav'


@pytest.fixture
def mock_system_path(monkeypatch, tmpdir):
    """
    Set a mocked environment for system path with some imaginary commands and
    non-commands included
    """
    dirs = []
    root = Path(tmpdir.strpath, 'root')
    for path in MOCK_PATH_DIRS:
        path = root.joinpath(path)
        path.mkdir(parents=True)
        dirs.append(str(path))
    for path in MOCK_PATH_SUBDIRS:
        root.joinpath(path).mkdir(parents=True)
    for path in MOCK_PATH_EXECUTABLES:
        filename = root.joinpath(path)
        with filename.open('wb') as handle:
            handle.flush()
            assert filename.exists()
        filename.chmod(MOCK_PERM_EXECUTABLE)
    for path in MOCK_PATH_NON_EXECUTABLES:
        filename = root.joinpath(path)
        with filename.open('wb') as handle:
            handle.flush()
            assert filename.exists()
        filename.chmod(MOCK_PERM_NON_EXECUTABLE)
        assert not os.access(str(filename), os.X_OK)

    monkeypatch.setenv('PATH', os.pathsep.join(dirs))
    return root


# pylint: disable=redefined-outer-name, unused-argument
def test_path_executables_load_posix(mock_system_path):
    """
    Test loading instance of path executables object in non-windows posix environments
    """
    Executables.__commands__ = None
    executables = Executables()
    assert isinstance(executables.__repr__(), str)
    assert executables.__repr__() == os.environ['PATH']

    for item in executables:
        print(item)
    assert len(executables) == MOCK_EXECUTABLE_COUNT_POSIX
    assert MOCK_COMMAND_AVAILABLE in executables
    assert isinstance(executables[MOCK_COMMAND_AVAILABLE], Path)
    # pylint: disable=use-implicit-booleaness-not-comparison
    assert list(executables) != []

    other = Executables()
    assert len(executables) == len(other)

    assert executables.get(MOCK_COMMAND_NOT_AVAILABLE) is None
    assert isinstance(executables.get(MOCK_COMMAND_AVAILABLE), Path)

    # Note: some systems have multiple sh on path
    paths = executables.paths(MOCK_COMMAND_AVAILABLE)
    assert len(paths) >= 1
    for path in paths:
        assert isinstance(path, Path)


# pylint: disable=redefined-outer-name, unused-argument
def test_path_executables_load_windows(mock_system_path, monkeypatch):
    """
    test loading of executables in mocked windows environment
    """
    monkeypatch.setattr('sys.platform', 'win32')
    Executables.__commands__ = None
    executables = Executables()
    assert executables.__platform_family__ == 'windows'
    assert len(executables) == MOCK_EXECUTABLE_COUNT_WINDOWS
    assert executables.get(MOCK_COMMAND_NOT_AVAILABLE) is None


# pylint: disable=redefined-outer-name, unused-argument
def test_path_executables_load_os_error(mock_system_path, monkeypatch):
    """
    Test loading instance of path executables object when file access causes OSError
    """
    monkeypatch.setattr('os.access', MockException(OSError))
    Executables.__commands__ = None
    executables = Executables()
    assert len(executables) == 0


def test_path_executables_invalid_directories(monkeypatch, tmpdir):
    """
    Test loading of path with invalid directory
    """
    missing = [str(Path(tmpdir).joinpath(f'dir{i}')) for i in range(1, 3)]
    monkeypatch.setenv('PATH', os.pathsep.join(missing))

    Executables.__commands__ = None
    executables = Executables()
    assert len(executables) == 0
