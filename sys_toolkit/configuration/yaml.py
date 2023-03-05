"""
Loader for configuration files in yaml format
"""
from pathlib import Path
from typing import Union

import yaml

from ..constants import DEFAULT_ENCODING
from ..exceptions import ConfigurationError
from .directory import ConfigurationFileDirectory
from .file import ConfigurationFile

YAML_FILE_EXTENSIONS = (
    '.yaml',
    '.yml',
)


class YamlConfiguration(ConfigurationFile):
    """
    Configuration parser for yaml configuration files
    """
    encoding = DEFAULT_ENCODING

    def load(self, path: Union[str, Path]) -> None:
        """
        Load specified YAML configuration file
        """
        path = self.__check_file_access__(path)

        try:
            with path.open('r', encoding=self.encoding) as handle:
                self.parse_data(yaml.safe_load(handle))
        except Exception as error:
            raise ConfigurationError(f'Error loading {path}: {error}') from error


class YamlConfigurationDirectory(ConfigurationFileDirectory):
    """
    Directory of yaml format configuration files
    """
    __file_loader_class__ = YamlConfiguration
    __extensions__ = YAML_FILE_EXTENSIONS
