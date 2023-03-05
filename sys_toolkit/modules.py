#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Utility classes for python module use
"""
from importlib.util import find_spec
from typing import List


def check_available_imports(*modules: List[str]):
    """
    Check named modules are available as imports for python

    This function can be used to ensure certain implementation of a functionality
    can be used without attempting to import the module and handling error
    """
    for module in modules:
        if find_spec(module) is None:
            return False
    return True
