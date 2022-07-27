"""
Darwin (macOS) secure temporary directory implementation
"""
from enum import Enum
from .base import ClipboardBaseClass


class DarwinClipboardType(Enum):
    """
    Various darwin clipboard types as passed to arguments of pbcopy and pbpaste commands
    """
    GENERAL = 'general'
    RULER = 'ruler'
    FIND = 'find'
    FONT = 'font'


class DarwinClipboard(ClipboardBaseClass):
    """
    Implementation of clipboard copy/paste base class for macOS darwin
    """
    __required_commands__ = ('pbcopy', 'pbpaste')

    def __init__(self, board=DarwinClipboardType.GENERAL):
        self.board = board

    @property
    def available(self):
        """
        Check if pbcopy and pbpaste commands are available on command line
        """
        return self.__check_required_cli_commands__()

    def clear(self):
        """
        Clear macOs clipboard by placing empty text into it
        """
        self.copy('')

    def copy(self, data):
        """
        Copy data to macOS clipboard
        """
        self.__copy_command_stdin__(data, ('pbcopy', '-pboard', self.board.value))

    def paste(self):
        """
        Paste data from macOS clipboard to variable
        """
        return self.__paste_command_stdout__(('pbpaste', '-pboard', self.board.value))
