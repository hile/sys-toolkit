"""
Common base class for clipboards
"""


class ClipboardBaseClass:
    """
    Base class implementation of clipboard copy and paste functions
    """
    def copy(self, data):
        """
        Copy data to clipboard
        """
        raise NotImplementedError('Clipboard copy() must be implemented in child class')

    def paste(self):
        """
        Get data from clipboard
        """
        raise NotImplementedError('Clipboard paste() must be implemented in child class')
