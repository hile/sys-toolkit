#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Darwin (macOS) secure temporary directory implementation
"""
from enum import Enum
from typing import Tuple

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
    board: DarwinClipboardType
    __required_commands__: Tuple = ('pbcopy', 'pbpaste')

    def __init__(self, board: DarwinClipboardType = DarwinClipboardType.GENERAL) -> None:
        self.board = board

    @property
    def available(self) -> bool:
        """
        Check if pbcopy and pbpaste commands are available on command line
        """
        return self.__check_required_cli_commands__()

    def clear(self) -> None:
        """
        Clear macOs clipboard by placing empty text into it
        """
        self.copy('')

    def copy(self, data: str) -> None:
        """
        Copy data to macOS clipboard
        """
        self.__copy_command_stdin__(data, ('pbcopy', '-pboard', self.board.value))

    def paste(self) -> str:
        """
        Paste data from macOS clipboard to variable
        """
        return self.__paste_command_stdout__(('pbpaste', '-pboard', self.board.value))
