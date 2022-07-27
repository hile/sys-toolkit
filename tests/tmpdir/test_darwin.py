"""
Unit tests for sys_toolkit.tmpdir.darwin module
"""
import pytest

from sys_toolkit.exceptions import SecureTemporaryDirectoryError
from sys_toolkit.tmpdir.darwin import DarwinSecureTemporaryDirectory


def test_tmpdir_darwin_properties():
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
