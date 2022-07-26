"""
Clipboard access for wayland display server clipboard
"""

from enum import Enum

from .base import ClipboardBaseClass


class WaylandClipboardSelectionType(Enum):
    """
    Enumerate the wayland clipboard selection types
    """
    PRIMARY = 'primary'


class WaylandClipboard(ClipboardBaseClass):
    """
    Clipboard copy / paste with wayland clipboard
    """
    __required_commands__ = ('wl-copy', 'wl-paste')

    def __init__(self, selection=WaylandClipboardSelectionType.PRIMARY):
        self.selection = selection

    @property
    def available(self):
        """
        Check if wl-copy and wl-paste commands are available on command line
        """
        return self.__check_required_cli_commands__()

    def copy(self, data):
        """
        Copy data to macOS clipboard
        """
        self.__copy_command_stdin__(data, *('wl-copy', f'--{self.selection.value}'))

    def paste(self):
        """
        Paste data from macOS clipboard to variable
        """
        return self.__paste_command_stdout__(*('wl-paste', '--no-newline', f'--{self.selection.value}'))
