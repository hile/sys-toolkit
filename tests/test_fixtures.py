#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Test shared  pytest mock fixtures
"""
import os

from pathlib import Path


# pylint: disable=unused-argument
def test_fixtures_mock_path_not_exists(mock_path_not_exists) -> None:
    """
    Test pathlib.Path.exists() returns always false
    """
    assert Path(__file__).exists() is False


# pylint: disable=unused-argument
def test_fixtures_mock_path_not_is_file(mock_path_not_file) -> None:
    """
    Test pathlib.Path.is_file() returns always false
    """
    assert Path(__file__).is_file() is False


# pylint: disable=unused-argument
def test_fixtures_mock_permission_denied(mock_permission_denied) -> None:
    """
    Test pathlib.Path.is_file() returns always false
    """
    assert os.access(__file__, os.R_OK) is False
