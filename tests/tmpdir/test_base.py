"""
Unit tests for sys_toolkit.tmpdir.base module
"""

import pytest

from sys_toolkit.tmpdir.base import SecureTemporaryDirectoryBaseClass

TEST_DATA = 'test string'
MOCK_VOLUME = '/dev/mock-dev'


class ImcompleteImplementation(SecureTemporaryDirectoryBaseClass):
    """
    Test incomplete implementation of SecureTemporaryDirectory
    """
    def __init__(self, suffix=None, prefix=None, dir=None):  # pylint: disable=redefined-builtin
        super().__init__(suffix, prefix, dir)  # pylint: disable=redefined-builtin
        self.volume = None

    def attach_storage_volume(self):
        """
        Call parent method that triggers the exception by default
        """
        print(f'attach mock device {self.volume}')

    def create_storage_volume(self):
        """
        Implement mocked method to set
        """
        self.volume = MOCK_VOLUME
        print('created volume')

    def detach_storage_volume(self):
        """
        Implement mocked method to detach and delete storage volume
        """
        self.volume = None


def test_tmpdir_base_properties():
    """
    Test properties of the base class for secure temporary directories
    """
    obj = SecureTemporaryDirectoryBaseClass()
    assert obj.path is None

    with pytest.raises(NotImplementedError):
        with SecureTemporaryDirectoryBaseClass() as obj:
            pass


def test_tmpdir_base_incomplete_properties():
    """
    Test properties of incomplete child class for secure temporary directory to catch cases
    where the functions quit early due to NotImplementedError
    """
    assert ImcompleteImplementation().volume is None

    with ImcompleteImplementation() as obj:
        assert obj.volume == MOCK_VOLUME

    directory = None
    with ImcompleteImplementation() as obj:
        directory = obj.path
        assert directory is not None
        assert directory.is_dir()
        # Run this explicitly to trigger call from __exit__ and to handle the 'if' case there
        obj.delete_storage_directory()

    assert not directory.is_dir()
