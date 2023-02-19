"""
Unit tests for cli_toolkit.subprocess module
"""

import os

from pathlib import Path

import pytest

from sys_toolkit.subprocess import run, run_command, run_command_lineoutput
from sys_toolkit.exceptions import CommandError

MIXED__ENCODINGS_FILE = Path(__file__).parent.joinpath('data/linefile_mixed_encodings')
VALID_COMMAND = 'uname'
INVALID_ARGS = (VALID_COMMAND, '--foobar')


def verify_string_list(value):
    """
    Test specified value is list of strings
    """
    assert isinstance(value, list)
    for line in value:
        assert isinstance(line, str)


def test_subprocess_run_uname_as_string(capfd):
    """
    Test running uname command with 'run'
    """
    run(VALID_COMMAND)
    captured = capfd.readouterr()
    assert captured.err == ''
    lines = captured.out.splitlines()
    assert len(lines) == 1


def test_subprocess_run_uname_as_string_invalid_cwd(tmpdir):
    """
    Test running uname command with 'run'
    """
    missing = Path(tmpdir.strpath, 'missing_directory')
    with pytest.raises(CommandError):
        run(VALID_COMMAND, cwd=missing)


def test_subprocess_run_uname_invalid_args():
    """
    Test running an invalid command with 'run' raising CommandError
    """
    with pytest.raises(CommandError):
        run(*INVALID_ARGS)


def test_subprocess_run_timeout_ok():
    """
    Test running an command with 'run' raising timeout
    """
    args = ['sleep', '1']
    run(*args, timeout=2)


def test_subprocess_run_timeout_exceeded():
    """
    Test running an command with 'run' raising timeout
    """
    args = ['sleep', '5']
    with pytest.raises(CommandError):
        run(*args, timeout=0.5)


def test_subprocess_run_command_uname_as_string():
    """
    Test running uname with 'run_command'
    """
    stdout, stderr = run_command(VALID_COMMAND)
    assert isinstance(stdout, bytes)
    assert isinstance(stderr, bytes)


def test_subprocess_run_command_uname_invalid_args():
    """
    Test running an invalid command with 'run_command' raising CommandError
    """
    with pytest.raises(CommandError):
        run(*INVALID_ARGS)


def test_subprocess_run_command_uname_with_env_path():
    """
    Test running uname with 'run_command' with custom invalid PATH

    Fails because command is not on path
    """
    env = os.environ.copy()
    env['PATH'] = '/foo:/bar'
    with pytest.raises(CommandError):
        run_command(VALID_COMMAND, env=env)


def test_subprocess_run_command_uname_as_args_list():
    """
    Test running uname with 'run_command' with arguments as list
    """
    args = [VALID_COMMAND]
    stdout, stderr = run_command(*args)
    assert isinstance(stdout, bytes)
    assert isinstance(stderr, bytes)


def test_subprocess_run_command_uname_as_args_tuple():
    """
    Test running uname with 'run_command' as tuple
    """
    args = [VALID_COMMAND]
    stdout, stderr = run_command(*args)
    assert isinstance(stdout, bytes)
    assert isinstance(stderr, bytes)


def test_subprocess_run_command_running_explicit_return_codes():
    """
    Test running an command with 'run_command' by specifying list of
    expected return codes
    """
    args = [VALID_COMMAND]
    stdout, stderr = run_command_lineoutput(*args, expected_return_codes=[0])
    assert isinstance(stdout, list)
    assert isinstance(stderr, list)


def test_subprocess_run_command_timeout_exceeded():
    """
    Test running an command with 'run_command' raising timeout
    """
    args = ['sleep', '1']
    run_command_lineoutput(*args, timeout=2)
    args = ['sleep', '5']
    with pytest.raises(CommandError):
        run_command_lineoutput(*args, timeout=0.5)


def test_subprocess_run_command_with_invalid_args():
    """
    Test running an invalid command with 'run_command'
    """
    with pytest.raises(CommandError):
        run_command(*INVALID_ARGS)


def test_subprocess_process_running_command_with_invalid_args():
    """
    Test running a command with 'run_command' and invalid args
    """
    with pytest.raises(CommandError):
        run_command(*INVALID_ARGS)


def test_subprocess_process_running_invalid_command():
    """
    Test running an invalid command with 'run_command'
    """
    with pytest.raises(CommandError):
        run_command('49FC61D4-F21B-4A0D-941D-9CC52F163CFF')


def test_subprocess_process_lineoutput_running_uname_as_string():
    """
    Test running uname command with 'run_command_lineoutput'
    """
    stdout, stderr = run_command_lineoutput(VALID_COMMAND)
    verify_string_list(stdout)
    verify_string_list(stderr)


def test_subprocess_process_lineoutput_running_uname_as_args_list():
    """
    Test running uname command with 'run_command_lineoutput'
    """
    args = [
        VALID_COMMAND,
    ]
    stdout, stderr = run_command_lineoutput(*args)
    verify_string_list(stdout)
    verify_string_list(stderr)


def test_subprocess_process_lineoutput_running_uname_as_args_tuple():
    """
    Test running uname command with 'run_command_lineoutput'
    """
    args = (
        VALID_COMMAND,
    )
    stdout, stderr = run_command_lineoutput(*args)
    verify_string_list(stdout)
    verify_string_list(stderr)


def test_subprocess_process_lineoutput_mixed_encoding_file_read():
    """
    Test reading data from a file with mixed encodings with 'run_command_lineoutput'
    """
    command = ('cat', MIXED__ENCODINGS_FILE.absolute())
    with pytest.raises(CommandError):
        run_command_lineoutput(*command)

    encodings = ['utf-8', 'latin1']
    stdout, stderr = run_command_lineoutput(*command, encodings=encodings)
    assert len(stdout) == 2
    assert len(stderr) == 0
    for line in stdout:
        assert isinstance(line, str)
