"""
Unit tests for sys_toolkit.clipboard.base module
"""
import pytest

from sys_toolkit.clipboard.base import ClipboardBaseClass

PASS_LINE = 'testpass123'
MIDDLE_LINE = 'Another line'
FINAL_LINE = 'Final line'
TEST_TEXT = '\n'.join([PASS_LINE, MIDDLE_LINE, FINAL_LINE])


def test_clipboard_base_class_properties():
    """
    Test properties of clipboard base class
    """
    obj = ClipboardBaseClass()
    assert obj.available is False

    assert obj.__check_required_modules__() is True
    assert obj.__check_required_env__() is True
    assert obj.__check_required_cli_commands__() is False

    with pytest.raises(NotImplementedError):
        obj.copy(TEST_TEXT)
    with pytest.raises(NotImplementedError):
        obj.paste()
