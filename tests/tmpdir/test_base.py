"""
Unit tests for sys_toolkit.tmpdir.base module
"""
from pathlib import Path
from typing import Optional, Union

from sys_toolkit.constants import DEFAULT_ENCODING
from sys_toolkit.tmpdir.base import SecureTemporaryDirectoryBaseClass

TEST_DATA = 'test string'
MOCK_VOLUME = '/dev/mock-dev'

TEST_LINK = 'link.txt'
TEST_FILES = (
    'testfile.txt',
    'test/testfile2.txt',
    'subdir/nested/deeper/testfile3.txt',
)


def create_test_files(path: Path) -> None:
    """
    Create test files and a link out of the directory to specified directory
    """
    path.joinpath(TEST_LINK).symlink_to(Path(__file__).resolve())
    for testfile in TEST_FILES:
        item = path.joinpath(testfile)
        if not item.parent.is_dir():
            item.parent.mkdir(parents=True)
        item.write_text(TEST_DATA, encoding=DEFAULT_ENCODING)


class ImcompleteImplementation(SecureTemporaryDirectoryBaseClass):
    """
    Test incomplete implementation of SecureTemporaryDirectory
    """
    def __init__(self,
                 suffix: str = None,
                 prefix: str = None,
                 parent_directory: Optional[Union[str, Path]] = None) -> None:
        super().__init__(suffix, prefix, parent_directory)
        self.volume = None

    def attach_storage_volume(self) -> None:
        """
        Call parent method that triggers the exception by default
        """
        print(f'attach mock device {self.volume}')

    def create_storage_volume(self) -> None:
        """
        Implement mocked method to set
        """
        self.volume = MOCK_VOLUME
        print('created volume')

    def detach_storage_volume(self) -> None:
        """
        Implement mocked method to detach and delete storage volume
        """
        self.volume = None


def test_tmpdir_base_properties() -> None:
    """
    Test properties of the base class for secure temporary directories
    """
    obj = SecureTemporaryDirectoryBaseClass()
    assert obj.path is None

    with SecureTemporaryDirectoryBaseClass() as obj:
        assert obj.__tmpdir__ is not None
        assert isinstance(obj.path, Path)


def test_tmpdir_base_incomplete_properties() -> None:
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


def test_tmpdir_base_files_list() -> None:
    """
    Test listing of files in the temporary directory, ignoring paths outside of the tmpdir
    """
    with SecureTemporaryDirectoryBaseClass() as obj:
        create_test_files(obj.path)
        assert len(obj.files) == 3


def test_tmpdir_base_files_list_directory_missing() -> None:
    """
    Test listing of files in the temporary directory when directory is removed when in use
    """
    with SecureTemporaryDirectoryBaseClass() as obj:
        obj.path.rmdir()
        assert len(obj.files) == 0
