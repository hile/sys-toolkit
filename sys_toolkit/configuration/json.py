#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Loader for configuration files in json format
"""
import json

from pathlib import Path
from typing import Optional, Union

from ..constants import DEFAULT_ENCODING
from ..exceptions import ConfigurationError
from .base import LoggingBaseClass
from .directory import ConfigurationFileDirectory
from .file import ConfigurationFile

JSON_FILE_EXTENSIONS = (
    '.json',
)


class JsonConfiguration(ConfigurationFile):
    """
    Configuration parser for JSON configuration files

    You can pass arguments to json.loads with loader_args
    """
    encoding = DEFAULT_ENCODING

    def __init__(self,
                 path: Union[str, Path] = None,
                 parent: Optional[LoggingBaseClass] = None,
                 debug_enabled: bool = False,
                 silent: bool = False,
                 **loader_args):
        self.__loader_args__ = loader_args
        super().__init__(path, parent=parent, debug_enabled=debug_enabled, silent=silent)

    def load(self, path: Union[str, Path]) -> None:
        """
        Load specified JSON configuration file
        """
        path = self.__check_file_access__(path)
        try:
            with path.open('r', encoding=self.encoding) as handle:
                self.parse_data(json.loads(handle.read(), **self.__loader_args__))
        except Exception as error:
            raise ConfigurationError(f'Error loading {path}: {error}') from error


class JsonConfigurationDirectory(ConfigurationFileDirectory):
    """
    Directory of JSON format configuration files
    """
    __file_loader_class__ = JsonConfiguration
    __extensions__ = JSON_FILE_EXTENSIONS
