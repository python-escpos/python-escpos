from .capabilities import CAPABILITIES


class CodePageManager:
    """Holds information about all the code pages (as defined
    in escpos-printer-db).
    """

    def __init__(self, data):
        self.data = data

    def get_all(self):
        return self.data.values()

    def encode(self, text, encoding, errors='strict'):
        """Adds support for Japanese to the builtin str.encode().

        TODO: Add support for custom code page data from
        escpos-printer-db.
        """
        # Python has not have this builtin?
        if encoding.upper() == 'KATAKANA':
            return encode_katakana(text)

        return text.encode(encoding, errors=errors)

    def get_encoding(self, encoding):
        # resolve the encoding alias
        return encoding.lower()


CodePages = CodePageManager(CAPABILITIES['encodings'])