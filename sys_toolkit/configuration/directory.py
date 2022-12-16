"""
Configuration file directory
"""

from pathlib import Path
from typing import Any, Optional

from ..exceptions import ConfigurationError
from .base import ConfigurationSection


class ConfigurationFileDirectory(ConfigurationSection):
    """
    Configuration file directory with individual configuration files loaded by matching
    file extensions.

    Class attribute __file_loader_class__ must be set to instance of ConfigurationFile
    or it's subclass in child class.

    Class attribute __extensions__ must list file extensions this directory loads.
    """
    __file_loader_class__ = None
    __extensions__ = ()

    def __init__(self,
                 path: Optional[str] = None,
                 parent: Optional[ConfigurationSection] = None,
                 debug_enabled: bool = False,
                 silent: bool = False):
        self.__path__ = Path(path).expanduser() if path is not None else None
        self.__files__ = []
        super().__init__(parent=parent, debug_enabled=debug_enabled, silent=silent)
        if self.__path__ is not None and self.__path__.exists():
            self.load(self.__path__)

    def __repr__(self) -> str:
        return str(self.__path__.name) if self.__path__ is not None else ''

    @property
    def file_loader_class(self) -> Any:
        """
        Return file loader class for loading the detected files
        """
        if self.__file_loader_class__ is None:
            raise ConfigurationError(f'__file_loader_class__ {self.__file_loader_class__} is not callable')
        return self.__file_loader_class__

    # pylint: disable=unused-argument
    def get_file_loader_class(self, path: Path) -> Any:
        """
        get file loader class for the configuration file directory laoder

        By default returns self.file_loader_class property.

        If the selected class depends on file override this method in child class.
        """
        return self.file_loader_class

    def load(self, directory) -> None:
        """
        Load all files in configuration file directory
        """
        if not isinstance(directory, Path):
            raise ConfigurationError(f'Not an instance of Path: {directory}')
        if not directory.is_dir():
            raise ConfigurationError(f'Not a directory: {directory}')

        for path in directory.iterdir():
            self.load_file(path)

    def load_file(self, path: Path) -> Any:
        """
        Load specified file path
        """
        if not path.is_file() or path.suffix not in self.__extensions__:
            return None

        file_loader_class = self.get_file_loader_class(path)
        # pylint: disable=not-callable
        item = file_loader_class(
            path,
            parent=self,
            debug_enabled=self.__debug_enabled__,
            silent=self.__silent__
        )
        self.__files__.append(item)
        return item
