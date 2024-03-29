#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Singleton instances for logging handlers

Logger initializes a singleton instance of named logging handlers, grouped by
handler name. Any registered log targets are available to all instances of the
logger group.
"""

import fnmatch
import logging
import logging.handlers
import sys

from pathlib import Path
from typing import Dict, Optional, Tuple, Union
from urllib.parse import urlparse

from .exceptions import LoggerError

DEFAULT_TARGET_NAME = 'default'
DEFAULT_LOGFORMAT = '%(asctime)s %(levelname)s %(message)s'
DEFAULT_LOG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DEFAULT_LOGFILE_FORMAT = '%(asctime)s %(module)s.%(funcName)s %(message)s'
DEFAULT_LOGFILE_SIZE_LIMIT = 2**20
DEFAULT_LOGFILE_BACKUP_COUNT = 10

DEFAULT_SYSLOG_FORMAT = '%(message)s'
DEFAULT_SYSLOG_LEVEL = logging.handlers.SysLogHandler.LOG_WARNING
DEFAULT_SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_USER

LOGGING_LEVEL_NAMES = ('DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
SYSLOG_LEVEL_MAP = {
    logging.handlers.SysLogHandler.LOG_DEBUG:   logging.DEBUG,
    logging.handlers.SysLogHandler.LOG_NOTICE:  logging.INFO,
    logging.handlers.SysLogHandler.LOG_INFO:    logging.INFO,
    logging.handlers.SysLogHandler.LOG_WARNING: logging.WARN,
    logging.handlers.SysLogHandler.LOG_ERR:     logging.ERROR,
    logging.handlers.SysLogHandler.LOG_CRIT:    logging.CRITICAL,
}


def get_default_syslog_address() -> Union[str, Tuple[str, int]]:
    """
    Return platform specific default address for syslog handler
    """
    if sys.platform[:5] == 'linux' or fnmatch.fnmatch(sys.platform, '*bsd*'):
        return '/dev/log'
    if sys.platform == 'darwin':
        return '/var/run/syslog'
    return ('localhost', 514)


class Logger:
    """
    Singleton class for extended loggers

    :param name: name of logger group, defaults to DEFAULT_TARGET_NAME
    :type name: str

    :param logformat: Log message format string, defaults to DEFAULT_LOGFORMAT
    :type name: str

    :param timeformat: Log message time format, defaults to DEFAULT_LOG_TIME_FORMAT
    :type name: str
    """

    groups: Dict = {}
    """LoggerGroup objects by group name"""
    name: Optional[str] = None
    """Name of this logger group"""

    def __init__(self,
                 name: Optional[str] = None,
                 logformat: str = DEFAULT_LOGFORMAT,
                 timeformat: str = DEFAULT_LOG_TIME_FORMAT) -> None:

        name = name if name is not None else DEFAULT_TARGET_NAME
        self.__dict__['_Loggergroups'] = Logger.groups
        self.name = name

        if name in Logger.groups:
            # Add back singleton instance initializer loggers
            for attr, value in Logger.groups[name].items():
                setattr(self, attr, value)
            self.__level__ = self.groups[name][name].level
        else:
            # Initialize logger group
            Logger.groups[name] = Logger.LoggerGroup(
                name,
                logformat,
                timeformat
            )
            setattr(self, name, self.groups[name][name])
            self.level = logging.Logger.root.level

    class LoggerGroup(dict):
        """
        Singleton implementation of logging configuration for named logging group
        """
        def __init__(self, name: str, logformat: str, timeformat: str) -> logging.Logger:
            super().__init__()
            self.name = name
            self.__register_stream_handler__(name, logformat, timeformat)
            self.__level__ = None

        def __get_or_create_logger__(self, name):
            """
            Get or create a named logger linked to singleton instance
            """
            if name not in self:
                for logging_manager in logging.Logger.manager.loggerDict.values():
                    if name == getattr(logging_manager, 'name', None):
                        self[name] = logging.getLogger(name)
                        break

            if name not in self:
                self[name] = logging.getLogger(name)

            return self[name]

        @staticmethod
        def __match_handlers__(handler_list, handler):
            """
            Match handlers by type and name, facility or method
            """
            def match_handler(item_a, item_b):  # pylint: disable=too-many-return-statements
                """
                Compare two handlers
                """
                if not isinstance(item_a, type(item_b)):
                    return False

                if isinstance(item_b, logging.handlers.RotatingFileHandler):
                    if item_a.baseFilename != item_b.baseFilename:
                        return False
                    return True

                if isinstance(item_b, logging.handlers.SysLogHandler):
                    for attr in ('address', 'facility'):
                        if getattr(item_a, attr) != getattr(item_b, attr):
                            return False
                    return True

                if isinstance(item_b, logging.handlers.HTTPHandler):
                    for attr in ('host', 'url', 'method'):
                        if getattr(item_a, attr) != getattr(item_b, attr):
                            return False
                    return True

                return True

            assert isinstance(handler_list, list)
            assert isinstance(handler, logging.Handler)

            for match in handler_list:
                if match_handler(match, handler):
                    return True

            return False

        def __register_stream_handler__(self,
                                        name: str,
                                        logformat: str,
                                        timeformat: str) -> logging.Logger:
            """
            Register stream handler to singleton instance
            """
            logger = self.__get_or_create_logger__(name)
            handler = logging.StreamHandler()

            if not self.__match_handlers__(logger.handlers, handler):
                handler.setFormatter(logging.Formatter(logformat, timeformat))
                logger.addHandler(handler)

            return logger

        def __register_syslog_handler__(self,
                                        name: str,
                                        address: Tuple[str, int],
                                        facility: int,
                                        default_level: int,
                                        socktype,
                                        logformat: str) -> logging.Logger:
            """
            Register syslog handler to singleton instance
            """
            logger = self.__get_or_create_logger__(name)
            handler = logging.handlers.SysLogHandler(address, facility, socktype)
            handler.level = default_level

            if not self.__match_handlers__(logger.handlers, handler):
                handler.setFormatter(logging.Formatter(logformat))
                logger.addHandler(handler)
                logger.setLevel(self.level)

            return logger

        def __register_http_handler__(self,
                                      name: str,
                                      url: str,
                                      method: str) -> logging.Logger:
            """
            Register HTTP handler to singleton instance
            """

            _scheme, netloc, _path = urlparse(url)[:3]
            if not netloc:
                raise LoggerError(f'Invalid URL: {url}')

            logger = self.__get_or_create_logger__(name)
            handler = logging.handlers.HTTPHandler(netloc, url, method)

            if not self.__match_handlers__(logger.handlers, handler):
                logger.addHandler(handler)
                logger.setLevel(self.level)

            return logger

        def __register_file_handler__(self,
                                      name: str,
                                      directory: Union[str, Path],
                                      filename: str,
                                      logformat: str,
                                      timeformat: str,
                                      max_bytes: int,
                                      backup_count: int) -> logging.Logger:
            """
            Register log file based logging handler to singleton instance
            """

            if filename is None:
                filename = f'{name}.log'

            path = Path(directory, filename)
            if not path.parent.is_dir():
                try:
                    path.parent.mkdir(parents=True)
                except OSError as error:
                    raise LoggerError(f'Error creating directory: {path.parent}') from error

            logger = self.__get_or_create_logger__(name)
            handler = logging.handlers.RotatingFileHandler(
                filename=path,
                mode='a+',
                maxBytes=max_bytes,
                backupCount=backup_count
            )

            if not self.__match_handlers__(logger.handlers, handler):
                handler.setFormatter(logging.Formatter(logformat, timeformat))
                logger.addHandler(handler)
                logger.setLevel(self.level)

            return logger

        @property
        def level(self) -> int:
            """
            Get log level
            """
            return self.__level__

        @level.setter
        def level(self, value: int) -> None:
            """
            Set log level
            """
            if not isinstance(value, int):
                if value in LOGGING_LEVEL_NAMES:
                    value = getattr(logging, value)
                try:
                    value = int(value)
                    assert value in SYSLOG_LEVEL_MAP.values()
                except ValueError as error:
                    raise LoggerError(f'Invalid logging level value: {value}') from error

            for logger in self.values():
                logger.setLevel(value)
            self.__level__ = value

    def __repr__(self) -> str:
        return str(self.name)

    @property
    def level(self) -> int:
        """
        Get or set logging level for all log handlers
        """
        return self.groups[self.name].level

    @level.setter
    def level(self, value: int) -> None:
        """
        Setter for logging level for all log handlers
        """
        self.groups[self.name].level = value

    def register_stream_handler(self,
                                name: str,
                                logformat: str = DEFAULT_LOGFORMAT,
                                timeformat: str = DEFAULT_LOG_TIME_FORMAT) -> logging.Logger:
        """
        Register a common log stream handler
        """
        logger = self.groups[self.name].__register_stream_handler__(
            name,
            logformat,
            timeformat
        )
        setattr(self, logger.name, logger)
        return logger

    def register_syslog_handler(self,
                                name: str,
                                address: Optional[Tuple[str, int]] = None,
                                facility: int = DEFAULT_SYSLOG_FACILITY,
                                default_level: int = DEFAULT_SYSLOG_LEVEL,
                                socktype: Optional[int] = None,
                                logformat: str = DEFAULT_SYSLOG_FORMAT) -> logging.Logger:
        """
        Register handler for syslog messages
        """
        if address is None:
            address = get_default_syslog_address()
        if default_level not in SYSLOG_LEVEL_MAP:
            raise LoggerError('Unsupported syslog level value')

        logger = self.groups[self.name].__register_syslog_handler__(
            name,
            address,
            facility,
            default_level,
            socktype,
            logformat
        )
        setattr(self, logger.name, logger)
        return logger

    def register_http_handler(self,
                              name: str,
                              url: str,
                              method: str = 'POST') -> logging.Logger:
        """
        Register a HTTP POST logging handler
        """
        logger = self.groups[self.name].__register_http_handler__(name, url, method)
        setattr(self, logger.name, logger)
        return logger

    def register_file_handler(self,
                              name: str,
                              directory: Union[str, Path],
                              filename: Optional[str] = None,
                              logformat: str = DEFAULT_LOGFILE_FORMAT,
                              timeformat: str = DEFAULT_LOG_TIME_FORMAT,
                              max_bytes: int = DEFAULT_LOGFILE_SIZE_LIMIT,
                              backup_count: int = DEFAULT_LOGFILE_BACKUP_COUNT) -> logging.Logger:

        """
        Register a common log file handler for rotating file based logs

        """
        logger = self.groups[self.name].__register_file_handler__(
            name,
            directory,
            filename,
            logformat,
            timeformat,
            max_bytes,
            backup_count
        )
        setattr(self, logger.name, logger)
        return logger
