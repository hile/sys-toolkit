#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Python unit test fixtures for sys_toolkit.tmpdir module
"""
from typing import Any, List, Dict, Iterator, Optional

import pytest

from sys_toolkit.constants import DEFAULT_ENCODING
from sys_toolkit.tests.mock import MockRun, MockReturnTrue

MOCK_DEVICE = '/dev/disk666'


# pylint: disable=too-few-public-methods
class MockDarwinInitMethods(MockRun):
    """
    Mock the various CLI commands used in initializing of darwin secure temporary directory
    """
    def __init__(self,
                 encoding: str = DEFAULT_ENCODING,
                 stdout: bytes = None,
                 stderr: bytes = None,
                 returncode: Optional[int] = None,
                 **kwargs: Dict[Any, Any]) -> None:
        super().__init__(encoding, stdout, stderr, returncode)
        self.returncode_hdid = kwargs.get('returncode_hdid', self.returncode)
        self.returncode_newfs_hfs = kwargs.get('returncode_newfs_hfs', self.returncode)
        self.returncode_mount = kwargs.get('returncode_mount', self.returncode)
        self.returncode_diskutil = kwargs.get('returncode_diskutil', self.returncode)

    def __call__(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> Any:
        """
        Check which command was called and return details accordingly
        """
        command = args[0]
        if command == 'hdid':
            # Command to create the storage volume
            self.stdout = bytes(f'{MOCK_DEVICE}\t\t', encoding=self.encoding)
            self.returncode = self.returncode_hdid
        elif command == 'newfs_hfs':
            # Command to create the storage volume
            self.stdout = bytes('', encoding=self.encoding)
            self.returncode = self.returncode_newfs_hfs
        elif command == 'mount':
            # Command to create the storage volume
            self.stdout = bytes('', encoding=self.encoding)
            self.returncode = self.returncode_mount
        elif command == 'diskutil':
            # Command to create the storage volume
            self.stdout = bytes('', encoding=self.encoding)
            self.returncode = self.returncode_diskutil
        else:
            raise NotImplementedError(f'Unexpected command: {command}')
        return super().__call__(*args, **kwargs)


@pytest.fixture
def mock_tmpdir_darwin_success(monkeypatch) -> Iterator[MockReturnTrue]:
    """
    Mock creating of darwin temporary directory successfully
    """
    mock_run = MockDarwinInitMethods()
    monkeypatch.setattr('sys_toolkit.tmpdir.base.Path.exists', MockReturnTrue())
    monkeypatch.setattr('sys_toolkit.tmpdir.darwin.run', mock_run)
    yield mock_run


@pytest.fixture
def mock_tmpdir_darwin_diskutil_fail(monkeypatch) -> Iterator[MockReturnTrue]:
    """
    Mock creating of darwin temporary directory with failure in ramdisk detaching
    """
    mock_run = MockDarwinInitMethods(returncode_diskutil=1)
    monkeypatch.setattr('sys_toolkit.tmpdir.base.Path.exists', MockReturnTrue())
    monkeypatch.setattr('sys_toolkit.tmpdir.darwin.run', mock_run)
    yield mock_run


@pytest.fixture
def mock_tmpdir_darwin_mount_fail(monkeypatch) -> Iterator[MockReturnTrue]:
    """
    Mock creating of darwin temporary directory with failure in ramdisk mounting
    """
    mock_run = MockDarwinInitMethods(returncode_mount=1)
    monkeypatch.setattr('sys_toolkit.tmpdir.base.Path.exists', MockReturnTrue())
    monkeypatch.setattr('sys_toolkit.tmpdir.darwin.run', mock_run)
    yield mock_run


@pytest.fixture
def mock_tmpdir_darwin_create_fail(monkeypatch) -> Iterator[MockDarwinInitMethods]:
    """
    Mock creating of darwin temporary directory with failure in ramdisk creation
    """
    mock_run = MockDarwinInitMethods(returncode_hdid=1)
    monkeypatch.setattr('sys_toolkit.tmpdir.base.Path.exists', MockReturnTrue())
    monkeypatch.setattr('sys_toolkit.tmpdir.darwin.run', mock_run)
    yield mock_run


@pytest.fixture
def mock_tmpdir_darwin_newfs_fail(monkeypatch) -> Iterator[MockReturnTrue]:
    """
    Mock creating of darwin temporary directory with failure in filesystem creation
    """
    mock_run = MockDarwinInitMethods(returncode_newfs_hfs=1)
    monkeypatch.setattr('sys_toolkit.tmpdir.base.Path.exists', MockReturnTrue())
    monkeypatch.setattr('sys_toolkit.tmpdir.darwin.run', mock_run)
    yield mock_run
