"""
Darwin (macOS) secure temporary directory implementation
"""
import os

from enum import Enum
from subprocess import run, PIPE, CalledProcessError

from ..exceptions import ClipboardError
from .base import ClipboardBaseClass

CLIPBOARD_LOCALE = 'en_US.UTF-8'


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

    @property
    def env(self):
        """
        Environment variables for commands
        """
        env = os.environ.copy()
        env['LANG'] = CLIPBOARD_LOCALE
        return env

    def copy(self, data):
        """
        Copy data to macOS clipboard
        """
        command = ('pbcopy', '-pboard', self.board.value)
        data = str(data).rstrip('\n')
        try:
            run(command, input=data.encode(), check=True, env=self.env)
        except CalledProcessError as error:
            raise ClipboardError(f'Error copying text to clipboad: {error}') from error

    def paste(self):
        """
        Paste data from macOS clipboard to variable
        """
        command = ('pbpaste', '-pboard', self.board.value)
        try:
            res = run(command, stdout=PIPE, check=True, env=self.env)
            return str(res.stdout, encoding='utf-8')
        except CalledProcessError as error:
            raise ClipboardError(f'Error copying text to clipboad: {error}') from error
