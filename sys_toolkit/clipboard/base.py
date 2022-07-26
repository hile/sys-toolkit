"""
Common base class for clipboards
"""

import os

from subprocess import run, CalledProcessError, PIPE

from ..exceptions import ClipboardError
from ..path import Executables
from ..modules import check_available_imports

CLIPBOARD_ENCODING = 'utf-8'
CLIPBOARD_LOCALE = 'en_US.UTF-8'


class ClipboardBaseClass:
    """
    Base class implementation of clipboard copy and paste functions
    """
    __required_commands__ = ()
    __required_modules__ = ()

    def __check_required_modules__(self):
        """
        Check if required python modules are available

        Returns true if no required modules are defined in __required_modules__
        """
        return check_available_imports(*self.__required_modules__)

    def __check_required_cli_commands__(self):
        """
        Check if required CLI commands are available
        """
        if not self.__required_commands__:
            return False
        executables = Executables()
        for command in self.__required_commands__:
            print(f'verify command in executables {command}')
            if command not in executables:
                return False
        return True

    def __copy_command_stdin__(self, data, *command):
        """
        Generic implementation to copy data from clipboard with specified CLI commmand
        and data from stdin to the command
        """
        data = str(data).rstrip('\n')
        try:
            run(command, input=data.encode(), check=True, env=self.env)
        except CalledProcessError as error:
            raise ClipboardError(f'Error copying text to clipboad: {error}') from error

    def __paste_command_stdout__(self, *command):
        """
        Generic implementation to paste data from stdout of specified CLI command
        """
        try:
            res = run(command, stdout=PIPE, check=True, env=self.env)
            return str(res.stdout, encoding=CLIPBOARD_ENCODING)
        except CalledProcessError as error:
            raise ClipboardError(f'Error copying text to clipboad: {error}') from error

    @property
    def env(self):
        """
        Environment variables for commands
        """
        env = os.environ.copy()
        env['LANG'] = CLIPBOARD_LOCALE
        return env

    @property
    def available(self):
        """
        Property to check if this type of clipboard is available

        Override in parent class with actual test. By default returns False
        """
        return False

    def copy(self, data):
        """
        Copy data to clipboard
        """
        raise NotImplementedError('Clipboard copy() must be implemented in child class')

    def paste(self):
        """
        Get data from clipboard
        """
        raise NotImplementedError('Clipboard paste() must be implemented in child class')
