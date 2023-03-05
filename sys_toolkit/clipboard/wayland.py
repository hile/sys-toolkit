#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Clipboard access for wayland display server clipboard
"""
from enum import Enum
from typing import Tuple

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
    selection: WaylandClipboardSelectionType
    __required_commands__: Tuple[str] = ('wl-copy', 'wl-paste')
    __required_env__: Tuple[str] = ('WAYLAND_DISPLAY',)

    def __init__(
            self,
            selection: WaylandClipboardSelectionType = WaylandClipboardSelectionType.PRIMARY) -> None:
        self.selection = selection

    @property
    def available(self) -> bool:
        """
        Check if wl-copy and wl-paste commands are available on command line
        """
        return self.__check_required_env__() and self.__check_required_cli_commands__()

    def clear(self) -> None:
        """
        Clear wayland clipboard
        """
        self.__run_command__(('wl-copy', '--clear'),)

    def copy(self, data: str) -> None:
        """
        Copy data to macOS clipboard
        """
        self.__copy_command_stdin__(data, ('wl-copy', f'--{self.selection.value}'))

    def paste(self) -> str:
        """
        Paste data from macOS clipboard to variable
        """
        return self.__paste_command_stdout__(('wl-paste', '--no-newline', f'--{self.selection.value}'))
