#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for sys_toolkit.configuration.file module
"""
from pathlib import Path

from sys_toolkit.configuration.file import ConfigurationFile


def test_configuration_file_no_file():
    """
    Test basic attributes of a ConfigurationFile object with not file path
    """
    obj = ConfigurationFile(path=None)
    assert obj.__path__ is None
    assert isinstance(obj.__repr__(), str)


def test_configuration_file_missing_file(tmpdir):
    """
    Test basic attributes of a ConfigurationFile object with missing file path
    """
    testfile = Path(tmpdir.strpath).joinpath('test.txt')
    assert not testfile.exists()
    obj = ConfigurationFile(path=testfile)
    assert obj.__path__ == testfile
    assert isinstance(obj.__repr__(), str)
