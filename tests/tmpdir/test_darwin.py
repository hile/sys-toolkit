"""
Unit tests for sys_toolkit.tmpdir.darwin module
"""
from pathlib import Path

import pytest

from sys_toolkit.exceptions import SecureTemporaryDirectoryError
from sys_toolkit.tmpdir.darwin import DarwinSecureTemporaryDirectory

from .conftest import MOCK_DEVICE


# pylint: disable=unused-argument
def test_tmpdir_darwin_properties(mock_tmpdir_darwin_success):
    """
    Test properties of a darwin secure temporary directory object that has not been initialized
    as a context manager
    """
    tmpdir = DarwinSecureTemporaryDirectory()
    assert tmpdir.path is None
    assert tmpdir.__device__ is None
    assert isinstance(tmpdir.size, int)

    with pytest.raises(SecureTemporaryDirectoryError):
        tmpdir.__check_ramdisk_device__()


def test_tmpdir_darwin_missing_ramdisk_device():
    """
    Test darwin temporary directory object check for ramdisk device when device is defined but missing
    """
    obj = DarwinSecureTemporaryDirectory()
    obj.__device__ = Path(MOCK_DEVICE)
    with pytest.raises(SecureTemporaryDirectoryError):
        obj.__check_ramdisk_device__()


# pylint: disable=unused-argument
def test_tmpdir_darwin_attach_storage_volume_uninitialized(mock_tmpdir_darwin_success):
    """
    Ensure attaching storage volume to uninitialized temporary volume fails early
    """
    with pytest.raises(SecureTemporaryDirectoryError):
        DarwinSecureTemporaryDirectory().attach_storage_volume()


# pylint: disable=unused-argument
def test_tmpdir_darwin_detach_storage_volume_uninitialized(mock_tmpdir_darwin_success):
    """
    Ensure detaching storage volume from uninitialized temporary volume fails early
    """
    with pytest.raises(SecureTemporaryDirectoryError):
        DarwinSecureTemporaryDirectory().detach_storage_volume()


# pylint: disable=unused-argument
def test_tmpdir_darwin_create_storage_volume(mock_tmpdir_darwin_success):
    """
    Test running create_storage_volume method directly for uninitialized darwin volumes
    """
    obj = DarwinSecureTemporaryDirectory()
    obj.create_storage_volume()
    assert obj.path is None
    assert obj.__device__ == Path(MOCK_DEVICE)


# pylint: disable=unused-argument
def test_tmpdir_darwin_context_manager_create_error(mock_tmpdir_darwin_create_fail):
    """
    Test initializing a darwin secure temporary directory when ramdisk creation fails
    """
    with pytest.raises(SecureTemporaryDirectoryError):
        with DarwinSecureTemporaryDirectory() as obj:
            obj  # pylint: disable=pointless-statement


# pylint: disable=unused-argument
def test_tmpdir_darwin_context_manager_newfs_error(mock_tmpdir_darwin_newfs_fail):
    """
    Test initializing a darwin secure temporary directory when filesystem creation fails
    """
    with pytest.raises(SecureTemporaryDirectoryError):
        with DarwinSecureTemporaryDirectory() as obj:
            obj  # pylint: disable=pointless-statement


# pylint: disable=unused-argument
def test_tmpdir_darwin_context_manager_mount_error(mock_tmpdir_darwin_mount_fail):
    """
    Test initializing a darwin secure temporary directory when filesystem mounting fails
    """
    with pytest.raises(SecureTemporaryDirectoryError):
        with DarwinSecureTemporaryDirectory() as obj:
            obj  # pylint: disable=pointless-statement


# pylint: disable=unused-argument
def test_tmpdir_darwin_context_manager_detach_error(mock_tmpdir_darwin_diskutil_fail):
    """
    Test initializing a darwin secure temporary directory when filesystem detaching fails
    """
    with pytest.raises(SecureTemporaryDirectoryError):
        with DarwinSecureTemporaryDirectory() as obj:
            obj  # pylint: disable=pointless-statement


# pylint: disable=unused-argument
def test_tmpdir_darwin_context_manager_ok(mock_tmpdir_darwin_success):
    """
    Test initializing a darwin secure temporary directory context manager successfully
    with mocked environment

    All CLI commands are mocked away
    """
    with DarwinSecureTemporaryDirectory() as obj:
        for attr in ('path', '__device__'):
            value = getattr(obj, attr)
            assert isinstance(value, Path)
        assert obj.path.is_dir()
