#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Test system process list parser module
"""

import pytest

from sys_toolkit.exceptions import CommandError
from sys_toolkit.tests.mock import MockRunCommandLineOutput
from sys_toolkit.process import Process, Processes, parse_datetime

from .conftest import MOCK_DATA

MOCK_PROCESSES_COUNT_FREEBSD = 105
MOCK_PROCESSES_COUNT_LINUX = 220
MOCK_PROCESSES_COUNT_MACOS = 558

UNEXPECTED_PROCESS = '1085 90560  1   0 27Nov21 ??   0:00.01 test this'
INVALID_DATETIMES = (
    '',
    None,
)


def validate_process_attributes(process) -> None:
    """
    Validate some attributes received from process list
    """
    repr_value = process.__repr__()
    assert isinstance(repr_value, str)
    assert repr_value != ''
    assert process.user_id is not None
    assert process.username is not None


def test_process_list_parse_date_invalid_formats() -> None:
    """
    Test various cases of invalid formats passed to 'parse_date' method and returned
    error value (always None, not raising ValueError)
    """
    for testcase in INVALID_DATETIMES:
        assert parse_datetime(testcase) is None


def test_process_validate_no_process_attributes() -> None:
    """
    Test loading a process entry from empty string and there are no process list
    attributes
    """
    processes = Processes()
    processes.attributes = []
    process = Process(processes, UNEXPECTED_PROCESS)
    assert process.started is None
    assert process.user_id is None
    assert process.username is None


def test_process_validate_missing_fields() -> None:
    """
    Test loading a process entry from empty string and there are no process list
    attributes
    """
    processes = Processes()
    process = Process(processes, UNEXPECTED_PROCESS)
    assert process.started is None
    assert process.user_id is None
    assert process.username is None


def test_process_list_load_freebsd(monkeypatch) -> None:
    """
    Test loading a process list when operating system is FreeBSD
    """
    mock_data = MockRunCommandLineOutput(MOCK_DATA.joinpath('processes.freebsd.txt'))
    monkeypatch.setattr('sys_toolkit.process.run_command_lineoutput', mock_data)

    processes = Processes()
    # pylint: disable=use-implicit-booleaness-not-comparison
    assert processes.__items__ == []
    processes.update()
    assert len(processes.__items__) == MOCK_PROCESSES_COUNT_FREEBSD
    for process in processes:
        validate_process_attributes(process)


def test_process_list_load_linux(monkeypatch) -> None:
    """
    Test loading a process list when operating system is linux
    """
    mock_data = MockRunCommandLineOutput(MOCK_DATA.joinpath('processes.linux.txt'))
    monkeypatch.setattr('sys_toolkit.process.run_command_lineoutput', mock_data)

    processes = Processes()
    # pylint: disable=use-implicit-booleaness-not-comparison
    assert processes.__items__ == []
    processes.update()
    assert len(processes.__items__) == MOCK_PROCESSES_COUNT_LINUX
    for process in processes:
        validate_process_attributes(process)


def test_process_list_load_macos(monkeypatch) -> None:
    """
    Test loading a process list when operating system is MacOS
    """
    mock_data = MockRunCommandLineOutput(MOCK_DATA.joinpath('processes.macos.txt'))
    monkeypatch.setattr('sys_toolkit.process.run_command_lineoutput', mock_data)

    processes = Processes()
    # pylint: disable=use-implicit-booleaness-not-comparison
    assert processes.__items__ == []
    processes.update()
    assert len(processes.__items__) == MOCK_PROCESSES_COUNT_MACOS
    for process in processes:
        validate_process_attributes(process)


def test_process_list_filter(monkeypatch) -> None:
    """
    Test filtering process list
    """
    mock_data = MockRunCommandLineOutput(MOCK_DATA.joinpath('processes.macos.txt'))
    monkeypatch.setattr('sys_toolkit.process.run_command_lineoutput', mock_data)

    processes = Processes()
    filtered = processes.filter(ruid=1085)
    assert len(filtered) < len(processes)
    assert len(filtered) == 333


def test_process_list_filter_invalid_filter(monkeypatch) -> None:
    """
    Test filtering process list
    """
    mock_data = MockRunCommandLineOutput(MOCK_DATA.joinpath('processes.macos.txt'))
    monkeypatch.setattr('sys_toolkit.process.run_command_lineoutput', mock_data)

    processes = Processes()
    with pytest.raises(CommandError):
        processes.filter('invalid')

    with pytest.raises(CommandError):
        processes.filter(invalid='invalid attribute')


def test_process_list_errors(monkeypatch) -> None:
    """
    Test processes with errors received during listing of processes
    """
    mock_data = MockRunCommandLineOutput(
        MOCK_DATA.joinpath('processes.macos.txt'),
        stderr='Errors listing processes'
    )
    monkeypatch.setattr('sys_toolkit.process.run_command_lineoutput', mock_data)

    processes = Processes()
    with pytest.raises(CommandError):
        list(processes)
