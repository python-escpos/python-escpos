#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the magic encode module

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: GNU GPL v3
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from nose.tools import raises, assert_raises
from hypothesis import given, example
import hypothesis.strategies as st
from escpos.magicencode import MagicEncode, Encoder
from escpos.katakana import encode_katakana
from escpos.exceptions import CharCodeError, Error



class TestEncoder:

    def test_can_encode(self):
        assert not Encoder({'cp437': 1}).can_encode('cp437', u'€')
        assert Encoder({'cp437': 1}).can_encode('cp437', u'á')
        assert not Encoder({'foobar': 1}).can_encode('foobar', 'a')

    def test_find_suitable_encoding(self):
        assert not Encoder({'cp437': 1}).find_suitable_encoding(u'€')
        assert Encoder({'cp858': 1}).find_suitable_encoding(u'€') == 'cp858'

    @raises(ValueError)
    def test_get_encoding(self):
        Encoder({}).get_encoding('latin1')


class TestMagicEncode:

    class TestInit:

        def test_disabled_requires_encoding(self, driver):
            with pytest.raises(Error):
                MagicEncode(driver, disabled=True)

    class TestWriteWithEncoding:

        def test_init_from_none(self, driver):
            encode = MagicEncode(driver, encoding=None)
            encode.write_with_encoding('cp858', '€ ist teuro.')
            assert driver.output == b'\x1bt\x13\xd5 ist teuro.'

        def test_change_from_another(self, driver):
            encode = MagicEncode(driver, encoding='cp437')
            encode.write_with_encoding('cp858', '€ ist teuro.')
            assert driver.output == b'\x1bt\x13\xd5 ist teuro.'

        def test_no_change(self, driver):
            encode = MagicEncode(driver, encoding='cp858')
            encode.write_with_encoding('cp858', '€ ist teuro.')
            assert driver.output == b'\xd5 ist teuro.'

    class TestWrite:

        def test_write(self, driver):
            encode = MagicEncode(driver)
            encode.write('€ ist teuro.')
            assert driver.output == b'\x1bt\x0f\xa4 ist teuro.'

        def test_write_disabled(self, driver):
            encode = MagicEncode(driver, encoding='cp437', disabled=True)
            encode.write('€ ist teuro.')
            assert driver.output == b'? ist teuro.'

        def test_write_no_codepage(self, driver):
            encode = MagicEncode(
                driver, defaultsymbol="_", encoder=Encoder({'cp437': 1}),
                encoding='cp437')
            encode.write(u'€ ist teuro.')
            assert driver.output == b'_ ist teuro.'

    class TestForceEncoding:

        def test(self, driver):
            encode = MagicEncode(driver)
            encode.force_encoding('cp437')
            assert driver.output == b'\x1bt\x00'

            encode.write('€ ist teuro.')
            assert driver.output == b'\x1bt\x00? ist teuro.'


try:
    import jcconv
except ImportError:
    jcconv = None


@pytest.mark.skipif(not jcconv, reason="jcconv not installed")
class TestKatakana:
    @given(st.text())
    @example("カタカナ")
    @example("あいうえお")
    @example("ﾊﾝｶｸｶﾀｶﾅ")
    def test_accept(self, text):
        encode_katakana(text)

    def test_result(self):
        assert encode_katakana('カタカナ') == b'\xb6\xc0\xb6\xc5'
        assert encode_katakana("あいうえお") == b'\xb1\xb2\xb3\xb4\xb5'


# TODO Idee für unittest: hypothesis-strings erzeugen, in encode_text werfen
# Ergebnis durchgehen: Vorkommnisse von Stuersequenzen suchen und daran den Text splitten in ein sortiertes dict mit Struktur:
# encoding: textfolge
# das alles wieder in unicode dekodieren mit den codepages und dann zusammenbauen
# fertigen String mit hypothesis-string vergleichen (Achtung bei katana-conversion. Die am besten auch auf den hypothesis-string
# anwenden)
# TODO bei nicht kodierbarem Zeichen Fehler werfen! Als Option das verhalten von jetzt hinzufügen
# TODO tests sollten eigentlich nicht gehen, wenn encode_char gerufen wird (extra_char ist nicht definiert)
# TODO verhalten bei leerem String festlegen und testen
