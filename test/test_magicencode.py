#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the magic encode module

:author: `Patrick Kanzler <dev@pkanzler.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""

import types
import typing

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

    class TestResetEncoding:
        """Tests for reset_encoding(), which discards cached encoding state.

        Some printers (e.g. NT-5890K) silently reset their active code page
        after commands such as font switches (ESC M) or hardware init (ESC @).
        reset_encoding() must be called after such commands so that the next
        write() re-emits CODEPAGE_CHANGE rather than sending text under the
        wrong code page.
        """

        def test_clears_encoding(self, driver: printer.Dummy) -> None:
            """reset_encoding sets self.encoding to None."""
            encode = MagicEncode(driver, encoding="CP437")
            encode.reset_encoding()
            assert encode.encoding is None

        def test_clears_used_encodings(self, driver: printer.Dummy) -> None:
            """reset_encoding empties the used_encodings set."""
            encode = MagicEncode(driver)
            encode.write("€")  # causes an encoding to be recorded in used_encodings
            assert len(encode.encoder.used_encodings) > 0
            encode.reset_encoding()
            assert encode.encoder.used_encodings == set()

        def test_next_write_reemits_codepage_change(self, driver: printer.Dummy) -> None:
            """After reset_encoding, the next write always emits CODEPAGE_CHANGE.

            Without reset, write_with_encoding skips the change command when
            the target encoding is already active.  After reset the cached
            encoding is None, so the change must be re-emitted even if the
            same encoding is chosen again.
            """
            encode = MagicEncode(driver, encoding="CP858")

            # CP858 already "active" — no CODEPAGE_CHANGE emitted for plain ASCII
            encode.write_with_encoding("CP858", "a")
            assert driver.output == b"a"

            encode.reset_encoding()
            encode.write_with_encoding("CP858", "a")
            # CODEPAGE_CHANGE (\x1bt) + slot 19 (\x13) must precede the character
            assert driver.output == b"a\x1bt\x13a"

        def test_reselects_encoding_by_slot_not_history(self, driver: printer.Dummy) -> None:
            """After reset, find_suitable_encoding ignores used_encodings history.

            Without clearing used_encodings, find_suitable_encoding prefers
            previously-used code pages (even high-slot ones) over lower-slot
            alternatives.  This caused the NT-5890K bug: € forced CP1257
            (slot 25) into used_encodings; after a font switch the printer
            reset its code page, but MagicEncode kept sending ü bytes encoded
            for CP1257 without re-emitting CODEPAGE_CHANGE — the printer read
            them against its reset code page and printed garbage.
            See https://github.com/python-escpos/python-escpos/pull/729

            After reset_encoding(), used_encodings is empty, so the sort in
            find_suitable_encoding falls back to slot order and picks the
            lowest-slot encoding that covers the character.
            """
            # Two encodings that can both encode ü; CP850 has the lower slot.
            encoder = Encoder({"CP850": 2, "CP858": 19})
            encode = MagicEncode(driver, encoder=encoder)

            # Simulate state left behind after printing € (CP858 was used)
            encode.encoder.used_encodings.add("CP858")
            encode.encoding = "CP858"

            # Without reset: history bias picks CP858 (previously used)
            assert encode.encoder.find_suitable_encoding("ü") == "CP858"

            # After reset: slot order wins — CP850 (slot 2) beats CP858 (slot 19)
            encode.reset_encoding()
            assert encode.encoder.find_suitable_encoding("ü") == "CP850"

        def test_set_font_change_resets_encoding(self, driver: printer.Dummy) -> None:
            """set() resets encoding when font actually changes."""
            driver.set(font="a")
            driver.magic.encoding = "CP858"
            driver.set(font="b")
            assert driver.magic.encoding is None

        def test_set_same_font_keeps_encoding(self, driver: printer.Dummy) -> None:
            """set() does NOT reset encoding when font is unchanged."""
            driver.set(font="a")
            driver.magic.encoding = "CP858"
            driver.set(font="a")
            assert driver.magic.encoding == "CP858"

        def test_set_with_default_no_font_change_keeps_encoding(self, driver: printer.Dummy) -> None:
            """set_with_default(align=...) must not reset encoding.

            set_with_default() always passes font="a" to set(), but if the
            font hasn't changed, reset_encoding() must not fire.
            """
            driver.set_with_default()  # sets font="a"
            driver.magic.encoding = "CP858"
            driver.set_with_default(align="right")
            assert driver.magic.encoding == "CP858"

        def test_hw_init_resets_font_tracking(self, driver: printer.Dummy) -> None:
            """hw("INIT") resets _font so the next set(font=...) always fires."""
            driver.set(font="a")
            assert driver._font == "a"
            driver.hw("INIT")
            assert driver._font is None


jaconv: typing.Optional[types.ModuleType]
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
