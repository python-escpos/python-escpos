#!/usr/bin/python
#  -*- coding: utf-8 -*-
""" Magic Encode

This module tries to convert an UTF-8 string to an encoded string for the printer.
It uses trial and error in order to guess the right codepage.
The code is based on the encoding-code in py-xml-escpos by @fvdsn.

:author: `Patrick Kanzler <dev@pkanzler.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 Patrick Kanzler and Frédéric van der Essen
:license: GNU GPL v3
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .constants import CHARCODE
from .exceptions import CharCodeError, Error
import copy
import six

try:
    import jcconv
except ImportError:
    jcconv = None

class MagicEncode(object):
    """ Magic Encode Class

    It tries to automatically encode utf-8 input into the right coding. When encoding is impossible a configurable
    symbol will be inserted.
    """
    def __init__(self, startencoding='PC437', force_encoding=False, defaultsymbol=b'', defaultencoding='PC437'):
        # running these functions makes sure that the encoding is suitable
        MagicEncode.codepage_name(startencoding)
        MagicEncode.codepage_name(defaultencoding)

        self.encoding = startencoding
        self.defaultsymbol = defaultsymbol
        if type(self.defaultsymbol) is not six.binary_type:
            raise Error("The supplied symbol {sym} has to be a binary string".format(sym=defaultsymbol))
        self.defaultencoding = defaultencoding
        self.force_encoding = force_encoding

    def set_encoding(self, encoding='PC437', force_encoding=False):
        """sets an encoding (normally not used)

        This function should normally not be used since it manipulates the automagic behaviour. However, if you want to
        force a certain codepage, then you can use this function.

        :param encoding: must be a valid encoding from CHARCODE
        :param force_encoding: whether the encoding should not be changed automatically
        """
        self.codepage_name(encoding)
        self.encoding = encoding
        self.force_encoding = force_encoding

    @staticmethod
    def codepage_sequence(codepage):
        """returns the corresponding codepage-sequence"""
        try:
            return CHARCODE[codepage][0]
        except KeyError:
            raise CharCodeError("The encoding {enc} is unknown.".format(enc=codepage))

    @staticmethod
    def codepage_name(codepage):
        """returns the corresponding codepage-name (for python)"""
        try:
            name = CHARCODE[codepage][1]
            if name == '':
                raise CharCodeError("The codepage {enc} does not have a connected python-codepage".format(enc=codepage))
            return name
        except KeyError:
            raise CharCodeError("The encoding {enc} is unknown.".format(enc=codepage))

    def encode_char(self, char):
        """
        Encodes a single unicode character into a sequence of
        esc-pos code page change instructions and character declarations
        """
        if type(char) is not six.text_type:
            raise Error("The supplied text has to be unicode, but is of type {type}.".format(
                type=type(char)
            ))
        encoded = b''
        encoding = self.encoding  # we reuse the last encoding to prevent code page switches at every character
        remaining = copy.copy(CHARCODE)

        while True:  # Trying all encoding until one succeeds
            try:
                if encoding == 'KATAKANA':  # Japanese characters
                    if jcconv:
                        # try to convert japanese text to half-katakanas
                        kata = jcconv.kata2half(jcconv.hira2kata(char))
                        if kata != char:
                            self.extra_chars += len(kata) - 1
                            # the conversion may result in multiple characters
                            return self.encode_str(kata)
                    else:
                        kata = char

                    if kata in TXT_ENC_KATAKANA_MAP:
                        encoded = TXT_ENC_KATAKANA_MAP[kata]
                        break
                    else:
                        raise ValueError()
                else:
                    try:
                        enc_name = MagicEncode.codepage_name(encoding)
                        encoded = char.encode(enc_name)
                        assert type(encoded) is bytes
                    except LookupError:
                        raise ValueError("The encoding {enc} seems to not exist in Python".format(enc=encoding))
                    except CharCodeError:
                        raise ValueError("The encoding {enc} is not fully configured in constants".format(
                            enc=encoding
                        ))
                    break

            except ValueError:  # the encoding failed, select another one and retry
                if encoding in remaining:
                    del remaining[encoding]
                if len(remaining) >= 1:
                    encoding = list(remaining)[0]
                else:
                    encoding = self.defaultencoding
                    encoded = self.defaultsymbol  # could not encode, output error character
                    break

        if encoding != self.encoding:
            # if the encoding changed, remember it and prefix the character with
            # the esc-pos encoding change sequence
            self.encoding = encoding
            encoded = CHARCODE[encoding][0] + encoded

        return encoded

    def encode_str(self, txt):
        # make sure the right codepage is set in the printer
        buffer = self.codepage_sequence(self.encoding)
        if self.force_encoding:
            buffer += txt.encode(self.codepage_name(self.encoding))
        else:
            for c in txt:
                buffer += self.encode_char(c)
        return buffer

    def encode_text(self, txt):
        """returns a byte-string with encoded text

        :param txt: text that shall be encoded
        :return: byte-string for the printer
        """
        if not txt:
            return

        self.extra_chars = 0

        txt = self.encode_str(txt)

        # if the utf-8 -> codepage conversion inserted extra characters,
        # remove double spaces to try to restore the original string length
        # and prevent printing alignment issues
        while self.extra_chars > 0:
            dspace = txt.find('  ')
            if dspace > 0:
                txt = txt[:dspace] + txt[dspace+1:]
                self.extra_chars -= 1
            else:
                break

        return txt


# todo emoticons mit charmap encoden
# todo Escpos liste von unterdrückten charcodes mitgeben
# TODO Sichtbarkeit der Methode anpassen (Eigentlich braucht man nur die set_encode und die encode_text)

TXT_ENC_KATAKANA_MAP = {
    # Maps UTF-8 Katakana symbols to KATAKANA Page Codes

    # Half-Width Katakanas
    '｡': b'\xa1',
    '｢': b'\xa2',
    '｣': b'\xa3',
    '､': b'\xa4',
    '･': b'\xa5',
    'ｦ': b'\xa6',
    'ｧ': b'\xa7',
    'ｨ': b'\xa8',
    'ｩ': b'\xa9',
    'ｪ': b'\xaa',
    'ｫ': b'\xab',
    'ｬ': b'\xac',
    'ｭ': b'\xad',
    'ｮ': b'\xae',
    'ｯ': b'\xaf',
    'ｰ': b'\xb0',
    'ｱ': b'\xb1',
    'ｲ': b'\xb2',
    'ｳ': b'\xb3',
    'ｴ': b'\xb4',
    'ｵ': b'\xb5',
    'ｶ': b'\xb6',
    'ｷ': b'\xb7',
    'ｸ': b'\xb8',
    'ｹ': b'\xb9',
    'ｺ': b'\xba',
    'ｻ': b'\xbb',
    'ｼ': b'\xbc',
    'ｽ': b'\xbd',
    'ｾ': b'\xbe',
    'ｿ': b'\xbf',
    'ﾀ': b'\xc0',
    'ﾁ': b'\xc1',
    'ﾂ': b'\xc2',
    'ﾃ': b'\xc3',
    'ﾄ': b'\xc4',
    'ﾅ': b'\xc5',
    'ﾆ': b'\xc6',
    'ﾇ': b'\xc7',
    'ﾈ': b'\xc8',
    'ﾉ': b'\xc9',
    'ﾊ': b'\xca',
    'ﾋ': b'\xcb',
    'ﾌ': b'\xcc',
    'ﾍ': b'\xcd',
    'ﾎ': b'\xce',
    'ﾏ': b'\xcf',
    'ﾐ': b'\xd0',
    'ﾑ': b'\xd1',
    'ﾒ': b'\xd2',
    'ﾓ': b'\xd3',
    'ﾔ': b'\xd4',
    'ﾕ': b'\xd5',
    'ﾖ': b'\xd6',
    'ﾗ': b'\xd7',
    'ﾘ': b'\xd8',
    'ﾙ': b'\xd9',
    'ﾚ': b'\xda',
    'ﾛ': b'\xdb',
    'ﾜ': b'\xdc',
    'ﾝ': b'\xdd',
    'ﾞ': b'\xde',
    'ﾟ': b'\xdf',
}
