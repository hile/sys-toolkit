#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Common base class for secure temporary directory objects
"""
import shutil

from pathlib import Path
from tempfile import mkdtemp
from typing import Any, List, Optional, Union

DEFAULT_TMPDIR_DIRECTORY = None
DEFAULT_TMPDIR_SUFFIX = None
DEFAULT_TMPDIR_PREFIX = 'secured.'


class SecureTemporaryDirectoryBaseClass:
    """
    Class to wrap a temporary directory to secure temporary storage
    """
    def __init__(self,
                 suffix: Optional[str] = None,
                 prefix: Optional[str] = None,
                 parent_directory: Optional[Union[str, Path]] = None) -> None:
        self.__suffix__ = suffix
        self.__prefix__ = prefix
        self.__parent_directory__ = parent_directory
        self.__tmpdir__ = None
        self.path = None

    def __check_directory__(self) -> bool:
        """
        Check target temporary directory is defined and the directory exists
        """
        return self.path and self.path.is_dir()

    def __enter__(self) -> Any:
        """
        Enter context manager, creating the temporary directory, volume and attaching the volume
        to the directory (by default volmes are skipped and temporary directory used as-is)
        """
        self.__tmpdir__ = mkdtemp(self.__suffix__, self.__prefix__, self.__parent_directory__)
        self.path = Path(self.__tmpdir__)
        self.create_storage_volume()
        self.attach_storage_volume()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Destruct the secure storage directory when object is removed
        """
        self.detach_storage_volume()
        self.delete_storage_directory()

    @property
    def files(self) -> List[Path]:
        """
        Find any files in the temporary directory

        This method excludes symlinks to files outside of the directory
        """
        files = []
        if not self.__check_directory__():
            return files
        for item in self.path.rglob('*'):
            if not item.is_file():
                continue
            if item.is_symlink():
                try:
                    item.resolve().relative_to(self.path)
                except ValueError:
                    # Skip file link to outside of the directory being iterated
                    continue
            files.append(item)
        return files

    def delete_storage_directory(self) -> None:
        """
        Method to destroy the created secure storage space directory in self.path

        This method is platform specific and by default raises NotImplementedError
        """
        if self.__check_directory__():
            shutil.rmtree(self.path)
        self.__tmpdir__ = None
        self.path = None

    def create_storage_volume(self) -> None:
        """
        Method to create a secure storage space

        This method is platform specific and by does nothing
        """
        return

    def attach_storage_volume(self) -> None:
        """
        Method to attach created secure storage space to self.path

        This method is platform specific and by does nothing
        """
        return

    def detach_storage_volume(self) -> None:
        """
        Method to detach created secure storage space from self.path

        This method is platform specific and by does nothing
        """
        return
