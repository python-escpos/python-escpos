#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the magic encode module

:author: `Patrick Kanzler <dev@pkanzler.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import hypothesis.strategies as st
import pytest
from hypothesis import example, given

from escpos import printer
from escpos.exceptions import Error
from escpos.katakana import encode_katakana
from escpos.magicencode import Encoder, MagicEncode


class TestEncoder:
    """
    Tests the single encoders.
    """

    def test_can_encode(self) -> None:
        assert not Encoder({"CP437": 1}).can_encode("CP437", "€")
        assert Encoder({"CP437": 1}).can_encode("CP437", "á")
        assert not Encoder({"foobar": 1}).can_encode("foobar", "a")

    def test_find_suitable_encoding(self) -> None:
        assert not Encoder({"CP437": 1}).find_suitable_encoding("€")
        assert Encoder({"CP858": 1}).find_suitable_encoding("€") == "CP858"

    def test_find_suitable_encoding_unnecessary_codepage_swap(self) -> None:
        enc = Encoder({"CP857": 1, "CP437": 2, "CP1252": 3, "CP852": 4, "CP858": 5})
        # desired behavior would be that the encoder always stays in the lower
        # available codepages if possible
        for character in ("Á", "É", "Í", "Ó", "Ú"):
            assert enc.find_suitable_encoding(character) == "CP857"

    def test_get_encoding(self) -> None:
        with pytest.raises(ValueError):
            Encoder({}).get_encoding_name("latin1")


class TestMagicEncode:
    """
    Tests the magic encode functionality.
    """

    class TestInit:
        """
        Test initialization.
        """

        def test_disabled_requires_encoding(self, driver: printer.Dummy) -> None:
            """
            Test that disabled without encoder raises an error.

            :param driver:
            """
            with pytest.raises(Error):
                MagicEncode(driver, disabled=True)

    class TestWriteWithEncoding:
        def test_init_from_none(self, driver: printer.Dummy) -> None:
            encode = MagicEncode(driver, encoding=None)
            encode.write_with_encoding("CP858", "€ ist teuro.")
            assert driver.output == b"\x1bt\x13\xd5 ist teuro."

        def test_change_from_another(self, driver: printer.Dummy) -> None:
            encode = MagicEncode(driver, encoding="CP437")
            encode.write_with_encoding("CP858", "€ ist teuro.")
            assert driver.output == b"\x1bt\x13\xd5 ist teuro."

        def test_no_change(self, driver: printer.Dummy) -> None:
            encode = MagicEncode(driver, encoding="CP858")
            encode.write_with_encoding("CP858", "€ ist teuro.")
            assert driver.output == b"\xd5 ist teuro."

    class TestWrite:
        def test_write(self, driver: printer.Dummy) -> None:
            encode = MagicEncode(driver)
            encode.write("€ ist teuro.")
            assert driver.output == b"\x1bt\x0f\xa4 ist teuro."

        def test_write_disabled(self, driver: printer.Dummy) -> None:
            encode = MagicEncode(driver, encoding="CP437", disabled=True)
            encode.write("€ ist teuro.")
            assert driver.output == b"? ist teuro."

        def test_write_no_codepage(self, driver: printer.Dummy) -> None:
            encode = MagicEncode(
                driver,
                defaultsymbol="_",
                encoder=Encoder({"CP437": 1}),
                encoding="CP437",
            )
            encode.write("€ ist teuro.")
            assert driver.output == b"_ ist teuro."

    class TestForceEncoding:
        def test(self, driver: printer.Dummy) -> None:
            encode = MagicEncode(driver)
            encode.force_encoding("CP437")
            assert driver.output == b"\x1bt\x00"

            encode.write("€ ist teuro.")
            assert driver.output == b"\x1bt\x00? ist teuro."


try:
    import jaconv
except ImportError:
    jaconv = None


@pytest.mark.skipif(not jaconv, reason="jaconv not installed")
class TestKatakana:
    @given(st.text())
    @example("カタカナ")
    @example("あいうえお")
    @example("ﾊﾝｶｸｶﾀｶﾅ")
    def test_accept(self, text: str) -> None:
        encode_katakana(text)

    def test_result(self) -> None:
        assert encode_katakana("カタカナ") == b"\xb6\xc0\xb6\xc5"
        assert encode_katakana("あいうえお") == b"\xb1\xb2\xb3\xb4\xb5"
