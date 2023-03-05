#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Parsers for text files with comments
"""
from pathlib import Path
from typing import Union

from .constants import DEFAULT_ENCODING
from .exceptions import FileParserError


class LineTextFile(list):
    """
    Generic base class for line based text file

    Loads the file as list of lines, skipping lines matched by self.skip_line and
    parsing lines to list items with self.parse_line.
    """
    comment_prefixes = '#'
    """Characters in start of line used to detect comments"""
    encoding = DEFAULT_ENCODING
    """Default encoding of file"""

    def __init__(self,
                 path: Union[str, Path],
                 comment_prefixes: str = None,
                 encoding: str = DEFAULT_ENCODING) -> None:
        super().__init__()
        if isinstance(comment_prefixes, str):
            self.comment_prefixes = comment_prefixes
        self.encoding = encoding
        self.path = Path(path)
        self.load()

    def load(self) -> None:
        """
        Load lines in file as list
        """
        if not self.path.is_file():
            raise FileParserError(f'No such file: {self.path}')

        with self.path.open('r', encoding=self.encoding) as filedescriptor:
            for line in filedescriptor.readlines():
                if self.skip_line(line):
                    continue
                item = self.parse_line(line.rstrip())
                if item is not None:
                    self.append(item)

    def skip_line(self, line: str) -> bool:
        """
        Check if line should be skipped

        By default checks if line starts with comment characters as defined
        in self.comment_prefixes or if line is empty.
        """
        return line.startswith(self.comment_prefixes) or not line.strip()

    def parse_line(self, line: str) -> str:
        """
        Parse line from file

        By default returns line trimmed of trailing whitespace
        """
        return line.rstrip()


class SortedLineTextFile(LineTextFile):
    """
    Sorted variant of line text file

    Extends LineTextFile by sorting loaded lines after loading
    """
    def __init__(self, path: Union[str, Path]) -> None:
        super().__init__(path)
        self.sort()
