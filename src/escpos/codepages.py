"""Helper module for code page handling."""
from .capabilities import CAPABILITIES


class CodePageManager:
    """Holds information about all the code pages.

    Information as defined in escpos-printer-db.
    """

    def __init__(self, data):
        """Initialize code page manager."""
        self.data = data

    @staticmethod
    def get_encoding_name(encoding):
        """Get encoding name.

        .. todo:: Resolve the encoding alias.
        """
        return encoding.upper()

    def get_encoding(self, encoding):
        """Return the encoding data."""
        return self.data[encoding]


CodePages = CodePageManager(CAPABILITIES["encodings"])
