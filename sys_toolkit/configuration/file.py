#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Configuration file parser base classes
"""
import os

from pathlib import Path
from typing import Any, Optional, Union

from ..exceptions import ConfigurationError
from .base import ConfigurationSection, LoggingBaseClass


class ConfigurationFile(ConfigurationSection):
    """
    Common base class for configuration file parsers
    """
    __default_paths__ = []

    def __init__(self,
                 path: Union[str, Path] = None,
                 parent: Optional[LoggingBaseClass] = None,
                 debug_enabled: bool = False,
                 silent: bool = False) -> None:
        self.__path__ = Path(path).expanduser() if path is not None else None
        super().__init__(parent=parent, debug_enabled=debug_enabled, silent=silent)

        # Load any common default paths
        for default_path in self.__default_paths__:
            default_path = Path(default_path)
            if default_path.is_file():
                self.load(default_path)

        # Load specified configuration file
        if self.__path__ is not None and self.__path__.exists():
            self.load(self.__path__)

    def __repr__(self) -> str:
        return str(self.__path__.name) if self.__path__ is not None else ''

    @staticmethod
    def __check_file_access__(path: Union[str, Path]) -> Path:
        """
        Check access to specified path as file

        Raises ConfigurationError if path is not a file or not readable
        """
        path = Path(path).expanduser()
        if not path.is_file():
            raise ConfigurationError(f'No such file: {path}')
        if not os.access(path, os.R_OK):
            raise ConfigurationError(f'Permission denied: {path}')
        return path

    def load(self, path: Union[str, Path]) -> None:
        """
        Load specified configuration file

        This method must be implemted in child class
        """
        raise NotImplementedError('File loading must be implemented in child class')

    def parse_data(self, data: Any) -> None:
        """
        Parse data read from configuration file

        Default implementation requires data is a dictionary
        """
        if data is None:
            return
        if not isinstance(data, dict):
            raise ConfigurationError(f'Data is not dict instance: {data}')
        self.__load_dictionary__(data)
