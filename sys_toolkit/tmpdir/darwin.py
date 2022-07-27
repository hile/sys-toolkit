"""
Secure temporary directory with ramdisk for macOS
"""

from pathlib import Path
from subprocess import PIPE

from ..exceptions import SecureTemporaryDirectoryError
from ..subprocess import run, CommandError

from .base import SecureTemporaryDirectoryBaseClass

# The units here are 512kb blocks i.e. this is 16MB
DEFAULT_SIZE_BLOCKS = 32768


class DarwinSecureTemporaryDirectory(SecureTemporaryDirectoryBaseClass):
    """
    Secure temporary directory for macOS darwin ramdisk
    """
    def __init__(self, suffix=None, prefix=None, parent_directory=None, size=DEFAULT_SIZE_BLOCKS):
        super().__init__(suffix, prefix, parent_directory)
        self.size = size
        self.__device__ = None

    def __check_ramdisk_device__(self):
        """
        Check ramdisk device
        """
        if not self.__device__:
            raise SecureTemporaryDirectoryError('Ramdisk device not initialized')
        if not self.__device__.exists():
            raise SecureTemporaryDirectoryError(f'No such ramdisk device: {self.__device__}')

    def create_storage_volume(self):
        """
        Create a secure ramdisk storage volume
        """
        try:
            command = ('hdid', '-drivekey', 'system-image=yes', '-nomount', f'ram://{self.size}')
            res = run(*command, stdout=PIPE, stderr=PIPE)
            self.__device__ = Path(str(res.stdout, encoding='utf-8').rstrip())
        except CommandError as error:
            raise SecureTemporaryDirectoryError(f'Error creating ramdisk: {error}') from error

        self.__check_ramdisk_device__()
        try:
            command = ('newfs_hfs', '-M', '700', self.__device__)
            run(*command, stdout=PIPE, stderr=PIPE)
        except CommandError as error:
            raise SecureTemporaryDirectoryError(
                'Error creating filesystem on ramdisk device {self.__device__}: {error'
            ) from error

    def attach_storage_volume(self):
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
            run(*command)
        except CommandError as error:
            raise SecureTemporaryDirectoryError(
                f'Error mounting {self.__device__} to {self.path}: {error}'
            ) from error

    def detach_storage_volume(self):
        """
        Detach created secure ramdisk storage volume
        """
        self.__check_ramdisk_device__()
        command = ('diskutil', 'quiet', 'eject', str(self.__device__))
        try:
            run(*command)
            self.__device__ = None
        except CommandError as error:
            raise SecureTemporaryDirectoryError(
                f'Error detaching ramdisk {self.__device__}: {error}'
            ) from error
