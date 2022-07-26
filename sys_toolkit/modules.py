"""
Utility classes for python module use
"""

from importlib.util import find_spec


def check_available_imports(*modules):
    """
    Check named modules are available as imports for python

    This function can be used to ensure certain implementation of a functionality
    can be used without attempting to import the module and handling error
    """
    for module in modules:
        if find_spec(module) is None:
            return False
    return True
