"""
Unit tests for vaskitsa.tests.packaging module
"""
from sys_toolkit.tests.packaging import validate_version_string


def test_version_string() -> None:
    """
    Test format of module version string validation
    """
    validate_version_string('1.0.0')
