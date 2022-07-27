"""
Utilities for operating system platform detection

Platform detection uses sys.platform to detect platform family
(darwin, linux, bsd, openbsd) and platform toolchain family
(gnu, bsd, openbsd)
"""

from enum import Enum

import sys
import re


class PlatformFamily(Enum):
    """
    Operating system families
    """
    DARWIN = 'darwin'
    LINUX = 'linux'
    BSD = 'bsd'
    OPENBSD = 'openbsd'
    WINDOWS = 'windows'


class ToolchainFamily(Enum):
    """
    Developer toolchain families
    """
    GNU = 'gnu'
    BSD = 'bsd'
    OPENBSD = 'openbsd'
    WINDOWS = 'windows'


# Group OS by platform
PLATFORM_PATTERNS = {
    PlatformFamily.DARWIN: {
        r'^darwin$',
    },
    PlatformFamily.LINUX: (
        r'^linux$',
        r'^linux\d+$',
    ),
    PlatformFamily.BSD: (
        r'^freebsd$',
        r'^freebsd\d+$',
    ),
    PlatformFamily.OPENBSD: (
        r'^openbsd$',
        r'^openbsd\d+$',
    ),
    PlatformFamily.WINDOWS: (
        r'^win32$',
    ),
}

# Group OS by primary toolchain platform
TOOLCHAIN_FAMILY_PATTERNS = {
    ToolchainFamily.GNU: (
        r'^linux$',
        r'^linux\d+$',
    ),
    ToolchainFamily.BSD: (
        r'^darwin$',
        r'^freebsd$',
        r'^freebsd\d+$',
    ),
    ToolchainFamily.OPENBSD: (
        r'^openbsd$',
        r'^openbsd\d+$',
    ),
    ToolchainFamily.WINDOWS: (
        r'^win32$',
    )
}


def detect_platform_family():
    """
    Detect OS platform family from sys.platform, grouping similar operating systems to single
    label based on PLATFORM_PATTERNS
    """
    for family, patterns in PLATFORM_PATTERNS.items():
        for pattern in patterns:
            if pattern == sys.platform or re.compile(pattern).match(sys.platform):
                return family.value
    raise ValueError(f'Error detecting OS platform family from {sys.platform}')


def detect_toolchain_family():
    """
    Detect CLI toolchain family from sys.platform, grouping similar operating system to singel
    label based on TOOLCHAIN_FAMILY_PATTERNS
    """
    for family, patterns in TOOLCHAIN_FAMILY_PATTERNS.items():
        for pattern in patterns:
            if pattern == sys.platform or re.compile(pattern).match(sys.platform):
                return family.value
    raise ValueError(f'Error detecting CLI toolchain family from {sys.platform}')
