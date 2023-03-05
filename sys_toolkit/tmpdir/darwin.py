#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Secure temporary directory with ramdisk for macOS
"""

from pathlib import Path
from subprocess import PIPE
from typing import Optional, Union

from ..constants import DEFAULT_ENCODING
from ..exceptions import SecureTemporaryDirectoryError
from ..subprocess import run, CommandError

from .base import SecureTemporaryDirectoryBaseClass

# The units here are 512kb blocks i.e. this is 16MB
DEFAULT_SIZE_BLOCKS = 32768


class DarwinSecureTemporaryDirectory(SecureTemporaryDirectoryBaseClass):
    """
    Secure temporary directory for macOS darwin ramdisk
    """
    def __init__(self,
                 suffix: Optional[str] = None,
                 prefix: Optional[str] = None,
                 parent_directory: Optional[Union[str, Path]] = None,
                 size: int = DEFAULT_SIZE_BLOCKS) -> None:
        super().__init__(suffix, prefix, parent_directory)
        self.size = size
        self.__device__ = None

    def __check_ramdisk_device__(self) -> None:
        """
        Check ramdisk device
        """
        if not self.__device__:
            raise SecureTemporaryDirectoryError('Ramdisk device not initialized')
        if not self.__device__.exists():
            raise SecureTemporaryDirectoryError(f'No such ramdisk device: {self.__device__}')

    def create_storage_volume(self) -> None:
        """
        Create a secure ramdisk storage volume
        """
        try:
            command = ('hdid', '-drivekey', 'system-image=yes', '-nomount', f'ram://{self.size}')
            res = run(*command, stdout=PIPE, stderr=PIPE)
            if res.returncode != 0:
                raise CommandError(res.stderr)
            self.__device__ = Path(str(res.stdout, encoding=DEFAULT_ENCODING).rstrip())
        except CommandError as error:
            raise SecureTemporaryDirectoryError(f'Error creating ramdisk: {error}') from error

        self.__check_ramdisk_device__()
        try:
            command = ('newfs_hfs', '-M', '700', self.__device__)
            res = run(*command, stdout=PIPE, stderr=PIPE)
            if res.returncode != 0:
                raise CommandError(res.stderr)
        except CommandError as error:
            raise SecureTemporaryDirectoryError(
                'Error creating filesystem on ramdisk device {self.__device__}: {error'
            ) from error

    def attach_storage_volume(self) -> None:
        """
        Attach created secure ramdisk storage volume
        """
        if not self.path:
            raise SecureTemporaryDirectoryError('Temporary directory path initialized')
        self.__check_ramdisk_device__()
        try:
            command = (
                'mount',
                '-t', 'hfs',
                '-o', 'noatime',
                '-o', 'nobrowse',
                str(self.__device__),
                str(self.path),
            )
            res = run(*command)
            if res.returncode != 0:
                raise CommandError(res.stderr)
        except CommandError as error:
            raise SecureTemporaryDirectoryError(
                f'Error mounting {self.__device__} to {self.path}: {error}'
            ) from error

    def detach_storage_volume(self) -> None:
        """
        Detach created secure ramdisk storage volume
        """
        self.__check_ramdisk_device__()
        command = ('diskutil', 'quiet', 'eject', str(self.__device__))
        try:
            res = run(*command)
            if res.returncode != 0:
                raise CommandError(res.stderr)
            self.__device__ = None
        except CommandError as error:
            raise SecureTemporaryDirectoryError(
                f'Error detaching ramdisk {self.__device__}: {error}'
            ) from error
