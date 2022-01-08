"""
Unit tests for sys_toolkit.system.darwin module
"""

from sys_toolkit.tests.mock import MockRunCommandLineOutput
from sys_toolkit.system.darwin import SoftwareVersion

from ..conftest import MOCK_DATA

SW_VERS_FILES = MOCK_DATA.joinpath('system/darwin')
SW_VERS_ATTRIBUTES = (
    'product_name',
    'product_version',
    'build_version',
)
SW_VERS_HIGH_SIERRA = 'Mac OS X'
SW_VERS_PRODUCT_NAMES = {
    'big_sur': 'macOS',
    'high_sierra': 'Mac OS X',
    'monterey': 'macOS',
}


def validate_software_version(obj):
    """
    Validate software version object that has not yet been lazy loaded
    """
    assert obj.__data__ == {}
    for attr in SW_VERS_ATTRIBUTES:
        value = getattr(obj, attr)
        assert isinstance(value, str)
        assert attr in obj.__data__
        assert getattr(obj, attr) == value
        obj.__data__ = {}

    assert isinstance(obj.__repr__(), str)


def test_darwin_software_version_high_sierra(monkeypatch):
    """
    Test loading software version data for MacOS 10.13 High Sierra
    """
    mock_output = MockRunCommandLineOutput(SW_VERS_FILES.joinpath('sw_vers.high_sierra'))
    monkeypatch.setattr('sys_toolkit.system.darwin.run_command_lineoutput', mock_output)
    obj = SoftwareVersion()
    validate_software_version(obj)
    assert obj.product_name == SW_VERS_PRODUCT_NAMES['high_sierra']


def test_darwin_software_version_big_sur(monkeypatch):
    """
    Test loading software version data for MacOS 11 Big Sur
    """
    mock_output = MockRunCommandLineOutput(SW_VERS_FILES.joinpath('sw_vers.big_sur'))
    monkeypatch.setattr('sys_toolkit.system.darwin.run_command_lineoutput', mock_output)
    obj = SoftwareVersion()
    validate_software_version(obj)
    assert obj.product_name == SW_VERS_PRODUCT_NAMES['big_sur']


def test_darwin_software_version_monterey(monkeypatch):
    """
    Test loading software version data for MacOS 12 Monterey
    """
    mock_output = MockRunCommandLineOutput(SW_VERS_FILES.joinpath('sw_vers.monterey'))
    monkeypatch.setattr('sys_toolkit.system.darwin.run_command_lineoutput', mock_output)
    obj = SoftwareVersion()
    assert obj.product_name == SW_VERS_PRODUCT_NAMES['monterey']
