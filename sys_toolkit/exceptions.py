#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Exceptions raised by OS base classes
"""


class ClipboardError(Exception):
    """
    Errors raised by clipbaord access
    """


class CommandError(Exception):
    """
    Exceptions raised by shell commands
    """


class ConfigurationError(Exception):
    """
    Errors raised by configuration processing
    """


class LoggerError(Exception):
    """
    Exceptions raised by logging configuration
    """


class FileParserError(Exception):
    """
    Exceptions raised while parsing text files
    """


class SecureTemporaryDirectoryError(Exception):
    """
    Exceptions raised while processing secure temporary directories
    """
