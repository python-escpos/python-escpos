from .capabilities import CAPABILITIES


class CodePageManager:
    """Holds information about all the code pages (as defined
    in escpos-printer-db).
    """

    def __init__(self, data):
        self.data = data

    def get_all(self):
        return self.data.values()

    @staticmethod
    def get_encoding_name(encoding):
        # TODO resolve the encoding alias
        return encoding.upper()

    def get_encoding(self, encoding):
        return self.data[encoding]


CodePages = CodePageManager(CAPABILITIES["encodings"])
