"""
Loader for configuration files in .ini format
"""
import configparser

from pathlib import Path
from typing import Optional, Union

from ..exceptions import ConfigurationError
from .base import LoggingBaseClass
from .directory import ConfigurationFileDirectory
from .file import ConfigurationFile

INI_FILE_EXTENSIONS = (
    '.ini',
)


class IniConfiguration(ConfigurationFile):
    """
    Configuration parser for INI style configuration files

    You can pass arguments to configparser.ConfigParser with
    loader_args
    """
    def __init__(self,
                 path: Union[str, Path] = None,
                 parent: Optional[LoggingBaseClass] = None,
                 debug_enabled: bool = False,
                 silent: bool = False,
                 **loader_args) -> None:
        self.__loader_args__ = loader_args
        super().__init__(path, parent=parent, debug_enabled=debug_enabled, silent=silent)

    def load(self, path: Union[str, Path]) -> None:
        """
        Load specified INI configuration file
        """
        path = self.__check_file_access__(path)
        parser = configparser.ConfigParser(**self.__loader_args__)
        try:
            parser.read(path)
        except Exception as error:
            raise ConfigurationError(f'Error loading {path}: {error}') from error

        for section_name in parser.sections():
            self.__load_section__(
                section_name,
                dict(parser[section_name].items())
            )


class IniConfigurationDirectory(ConfigurationFileDirectory):
    """
    Directory of ini format configuration files
    """
    __file_loader_class__ = IniConfiguration
    __extensions__ = INI_FILE_EXTENSIONS
