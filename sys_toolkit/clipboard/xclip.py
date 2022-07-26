"""
Clipboard access for X11 with xclip CLI command clipboard
"""

from enum import Enum

from .base import ClipboardBaseClass


class XclipClipboardSelectionType(Enum):
    """
    Enumerate the X11 clipboard selection types
    """
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    CLIPBOARD = 'clipboard'


class XclipClipboard(ClipboardBaseClass):
    """
    Clipboard copy / paste with wayland clipboard
    """
    __required_commands__ = ('xclip',)
    __required_env__ = ('DISPLAY',)

    def __init__(self, selection=XclipClipboardSelectionType.PRIMARY):
        self.selection = selection

    @property
    def available(self):
        """
        Check if wl-copy and wl-paste commands are available on command line
        """
        return self.__check_required_env__() and self.__check_required_cli_commands__()

    def copy(self, data):
        """
        Copy data to macOS clipboard
        """
        self.__copy_command_stdin__(data, *('xclip', '-selection', self.selection.value, '-in'))

    def paste(self):
        """
        Paste data from macOS clipboard to variable
        """
        return self.__paste_command_stdout__(*('xclip', '-selection', self.selection.value, '-out'))
