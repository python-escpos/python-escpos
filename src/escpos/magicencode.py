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

from .constants import CODEPAGE_CHANGE
from .exceptions import CharCodeError, Error
from .capabilities import get_profile
import copy
import six

try:
    import jcconv
except ImportError:
    jcconv = None


def encode_katakana(text):
    """I don't think this quite works yet."""
    encoded = []
    for char in text:
        if jcconv:
            # try to convert japanese text to half-katakanas
            char = jcconv.kata2half(jcconv.hira2kata(char))
            # TODO: "the conversion may result in multiple characters"
            # When? What should we do about it?

        if char in TXT_ENC_KATAKANA_MAP:
            encoded.append(TXT_ENC_KATAKANA_MAP[char])
        else:
            encoded.append(char)
    print(encoded)
    return b"".join(encoded)



# TODO: When the capabilities.yml format is finished, this should be
# in the profile itself.
def get_encodings_from_profile(profile):
    mapping = {k: v.lower() for k, v in profile.codePageMap.items()}
    if hasattr(profile, 'codePages'):
        code_pages = [n.lower() for n in profile.codePages]
        return {k: v for k, v in mapping.items() if v in code_pages}
    else:
        return mapping


class CodePages:
    def get_all(self):
        return get_encodings_from_profile(get_profile()).values()

    def encode(self, text, encoding, errors='strict'):
        # Python has not have this builtin?
        if encoding.upper() == 'KATAKANA':
            return encode_katakana(text)

        return text.encode(encoding, errors=errors)

    def get_encoding(self, encoding):
        # resolve the encoding alias
        return encoding.lower()

code_pages = CodePages()


class Encoder(object):
    """Takes a list of available code spaces. Picks the right one for a
    given character.

    Note: To determine the codespace, it needs to do the conversion, and
    thus already knows what the final byte in the target encoding would
    be. Nevertheless, the API of this class doesn't return the byte.

    The caller use to do the character conversion itself.

        $ python -m timeit -s "{u'ö':'a'}.get(u'ö')"
        100000000 loops, best of 3: 0.0133 usec per loop

        $ python -m timeit -s "u'ö'.encode('latin1')"
        100000000 loops, best of 3: 0.0141 usec per loop
    """

    def __init__(self, codepages):
        self.codepages = codepages
        self.reverse = {v:k for k, v in codepages.items()}
        self.available_encodings = set(codepages.values())
        self.used_encodings = set()

    def get_sequence(self, encoding):
        return self.reverse[encoding]

    def get_encoding(self, encoding):
        """resolve aliases

        check that the profile allows this encoding
        """
        encoding = code_pages.get_encoding(encoding)
        if not encoding in self.available_encodings:
            raise ValueError('This encoding cannot be used for the current profile')
        return encoding

    def get_encodings(self):
        """
        - remove the ones not supported
        - order by used first, then others
        - do not use a cache, because encode already is so fast
        """
        return self.available_encodings

    def can_encode(self, encoding, char):
        try:
            encoded = code_pages.encode(char, encoding)
            assert type(encoded) is bytes
            return encoded
        except LookupError:
            # We don't have this encoding
            return False
        except UnicodeEncodeError:
            return False

        return True

    def find_suitable_codespace(self, char):
        """The order of our search is a specific one:

        1. code pages that we already tried before; there is a good
           chance they might work again, reducing the search space,
           and by re-using already used encodings we might also
           reduce the number of codepage change instructiosn we have
           to send. Still, any performance gains will presumably be
           fairly minor.

        2. code pages in lower ESCPOS slots first. Presumably, they
           are more likely to be supported, so if a printer profile
           is missing or incomplete, we might increase our change
           that the code page we pick for this character is actually
           supported.

        # XXX actually do speed up the search
        """
        for encoding in self.get_encodings():
            if self.can_encode(encoding, char):
                # This encoding worked; at it to the set of used ones.
                self.used_encodings.add(encoding)
                return encoding


class MagicEncode(object):
    """ Magic Encode Class

    It tries to automatically encode utf-8 input into the right coding. When encoding is impossible a configurable
    symbol will be inserted.

    encoding: If you know the current encoding of the printer when
    initializing this class, set it here. If the current encoding is
    unknown, the first character emitted will be a codepage switch.
    """
    def __init__(self, driver, encoding=None, disabled=False,
                 defaultsymbol='?', encoder=None):
        if disabled and not encoding:
            raise Error('If you disable magic encode, you need to define an encoding!')

        self.driver = driver
        self.encoder = encoder or Encoder(get_encodings_from_profile(driver.profile))

        self.encoding = self.encoder.get_encoding(encoding) if encoding else None
        self.defaultsymbol = defaultsymbol
        self.disabled = disabled

    def force_encoding(self, encoding):
        """Sets a fixed encoding. The change is emitted right away.

        From now one, this buffer will switch the code page anymore.
        However, it will still keep track of the current code page.
        """
        if not encoding:
            self.disabled = False
        else:
            self.write_with_encoding(encoding, None)
            self.disabled = True

    def write(self, text):
        """Write the text, automatically switching encodings.
        """

        if self.disabled:
            self.write_with_encoding(self.encoding, text)
            return

        # TODO: Currently this very simple loop means we send every
        # character individually to the printer. We can probably
        # improve performace by searching the text for the first
        # character that cannot be rendered using the current code
        # page, and then sending all of those characters at once.
        # Or, should a lower-level buffer be responsible for that?

        for char in text:
            # See if the current code page works for this character.
            # The encoder object will use a cache to be able to answer
            # this question fairly easily.
            if self.encoding and self.encoder.can_encode(self.encoding, char):
                self.write_with_encoding(self.encoding, char)
                continue

            # We have to find another way to print this character.
            # See if any of the code pages that the printer profile supports
            # can encode this character.
            codespace = self.encoder.find_suitable_codespace(char)
            if not codespace:
                self._handle_character_failed(char)
                continue

            self.write_with_encoding(codespace, char)

    def _handle_character_failed(self, char):
        """Called when no codepage was found to render a character.
        """
        # Writing the default symbol via write() allows us to avoid
        # unnecesary codepage switches.
        self.write(self.defaultsymbol)

    def write_with_encoding(self, encoding, text):
        if text is not None and type(text) is not six.text_type:
            raise Error("The supplied text has to be unicode, but is of type {type}.".format(
                type=type(text)
            ))

        encoding = self.encoder.get_encoding(encoding)

        # We always know the current code page; if the new codepage
        # is different, emit a change command.
        if encoding != self.encoding:
            self.encoding = encoding
            self.driver._raw(b'{}{}'.format(
                CODEPAGE_CHANGE,
                six.int2byte(self.encoder.get_sequence(encoding))
            ))

        if text:
            self.driver._raw(code_pages.encode(text, encoding, errors="replace"))


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
