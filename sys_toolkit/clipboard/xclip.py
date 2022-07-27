"""
Clipboard access for X11 with xclip CLI command clipboard
"""

from enum import Enum

from .base import ClipboardBaseClass, CLIPBOARD_ENCODING

XCLIP_CLIPBOARD_EMPTY_ERROR = 'Error: target STRING not available'


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
    __required_commands__ = ('xclip', 'xsel',)
    __required_env__ = ('DISPLAY',)

    def __init__(self, selection=XclipClipboardSelectionType.PRIMARY):
        self.selection = selection

    def __process_paste_error__(self, response):
        """
        Process return value for paste command error specific to xclip

        Xclip returns an error string with code 1 when clipboard is empty
        """
        if response.returncode == 1:
            error = str(response.stderr, encoding=CLIPBOARD_ENCODING).strip()
            if error == XCLIP_CLIPBOARD_EMPTY_ERROR:
                return None
        return super().__process_paste_error__(response)

    @property
    def available(self):
        """
        Check if wl-copy and wl-paste commands are available on command line
        """
        return self.__check_required_env__() and self.__check_required_cli_commands__()

    def clear(self):
        """
        Clear data on clipboards with xsel
        """
        self.__run_command__('xsel', '-c')
        self.__run_command__('xsel', '-bc')

    def copy(self, data):
        """
        Copy data to macOS clipboard
        """
        self.__copy_command_stdin__(data, ('xclip', '-selection', self.selection.value, '-in'))

    def paste(self):
        """
        Paste data from macOS clipboard to variable
        """
        return self.__paste_command_stdout__(('xclip', '-selection', self.selection.value, '-out'))
