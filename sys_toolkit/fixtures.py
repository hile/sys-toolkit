#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Shared fixtures for unit tests
"""
import os

from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List

import pytest


@pytest.fixture
def mock_path_mkdir_permission_denied(monkeypatch) -> Iterator[Callable]:
    """
    Fixture to mock pathlib.Path.exists to return false
    """
    # pylint: disable=unused-argument
    def permission_error(*args: List[Any], **kwargs: Dict):
        """
        Always return false for os.access
        """
        raise OSError('Permission denied')

    monkeypatch.setattr(Path, 'mkdir', permission_error)
    yield permission_error


@pytest.fixture
def mock_path_not_exists(monkeypatch) -> Iterator[Callable]:
    """
    Fixture to mock pathlib.Path.exists to return false
    """
    # pylint: disable=unused-argument
    def not_exists(*args: List[Any]) -> bool:
        """
        Always return false for os.access
        """
        return False

    monkeypatch.setattr(Path, 'exists', not_exists)
    yield not_exists


@pytest.fixture
def mock_path_not_file(monkeypatch) -> Iterator[Callable]:
    """
    Fixture to mock pathlib.Path.is_file to return false
    """
    # pylint: disable=unused-argument
    def not_is_file(*args: List[Any]) -> bool:
        """
        Always return false for is_file
        """
        return False

    monkeypatch.setattr(Path, 'is_file', not_is_file)
    yield not_is_file


@pytest.fixture
def mock_permission_denied(monkeypatch) -> Iterator[Callable]:
    """
    Fixture to mock os.access returning false
    """
    # pylint: disable=unused-argument
    def permission_denied(*args: List[Any]) -> bool:
        """
        Always return false for os.access
        """
        return False

    monkeypatch.setattr(os, 'access', permission_denied)
    yield permission_denied
