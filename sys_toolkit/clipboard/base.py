"""
Common base class for clipboards
"""

from ..path import Executables
from ..modules import check_available_imports


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
            if command not in executables:
                return False
        return True

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
