#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Common base class for scripts with configurable logging
"""
import os
import sys

from typing import Any, Dict, List, Optional

from sys_toolkit.logger import Logger


class LoggingBaseClass:
    """
    Common base class with logging method using Logger objects
    """
    __debug_enabled__: bool
    __silent__: bool
    __env_vars__: Dict = {
        'debug_enabled': 'DEBUG',
        'silent': 'SILENT',
    }

    def __init__(self,
                 debug_enabled: bool = False,
                 silent: bool = False,
                 logger: Optional[str] = None):
        self.__debug_enabled__ = debug_enabled or os.environ.get(self.__env_vars__['debug_enabled'], False)
        self.__silent__ = silent or os.environ.get(self.__env_vars__['silent'], False)

        # Generic logging class for compatibility
        self.logger = Logger(logger)

    @property
    def __is_debug_enabled__(self) -> bool:
        """
        Check if debugging is enabled
        """
        return self.__debug_enabled__

    @property
    def __is_silent__(self) -> bool:
        """
        Check if silent mode is enabled
        """
        return self.__silent__

    @staticmethod
    def __parse_string_args__(*args: List[Any]) -> str:
        """
        Parse list of values as stripped string concatenated by space
        """
        args = [str(arg).rstrip() for arg in args]
        return ' '.join(args)

    def debug(self, *args: List[Any]) -> None:
        """
        Send debug message to stderr if debug mode is enabled
        """
        if not self.__is_debug_enabled__:
            return
        self.error(*args)

    def error(self, *args: List[Any]) -> None:
        """
        Send error message to stderr
        """
        sys.stderr.write(f'{self.__parse_string_args__(*args)}\n')
        sys.stderr.flush()

    def message(self, *args: List[Any]) -> None:
        """
        Show message to stdout unless silent flag is set
        """
        if self.__is_silent__:
            return
        sys.stdout.write(f'{self.__parse_string_args__(*args)}\n')
        sys.stdout.flush()
