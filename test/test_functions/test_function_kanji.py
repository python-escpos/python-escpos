import pytest
import escpos.printer as printer
from escpos.constants import (
    KANJI_ENTER_KANJI_MODE,
    KANJI_EXIT_KANJI_MODE,
    KANJI_PRINT_MODE,
    KANJI_UNDERLINE,
    KANJI_SET_ENCODING,
    KANJI_DEFINE_USER_DEFINED,
    KANJI_DELETE_USER_DEFINED,
    KANJI_SET_SPACING,
    KANJI_SET_CHAR_STYLE,
    KANJI_SET_QUADRUPLE_SIZE,
)

checkerboard_kanji = (
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\xf0\xf0\xf0"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
    b"\x0f\x0f\x0f"
)


def test_enter_kanji_mode() -> None:
    """should enter kanji mode."""
    instance = printer.Dummy()
    instance._enter_kanji_mode()
    assert instance.output == KANJI_ENTER_KANJI_MODE


def test_exit_kanji_mode() -> None:
    """should exit kanji mode."""
    instance = printer.Dummy()
    instance._exit_kanji_mode()
    assert instance.output == KANJI_EXIT_KANJI_MODE


def test_kanji_text_ISO_2022_JP() -> None:
    """should print kanji text."""
    instance = printer.Dummy()
    instance.set_kanji_encoding("iso2022_jp")
    instance.kanji_text("Hello世界Hello")
    assert instance.output == (
        KANJI_SET_ENCODING
        + b"\x00"
        + b"\x48\x65\x6c\x6c\x6f"
        + KANJI_ENTER_KANJI_MODE
        + b"\x40\x24\x33\x26"
        + KANJI_EXIT_KANJI_MODE
        + b"\x48\x65\x6c\x6c\x6f"
    )


def test_kanji_text_shift_jis() -> None:
    """should print kanji text."""
    instance = printer.Dummy()
    instance.set_kanji_encoding("shift_jis")
    instance.kanji_text("Hello世界Hello")
    assert instance.output == (
        KANJI_SET_ENCODING
        + b"\x01"
        + KANJI_ENTER_KANJI_MODE
        + b"\x48\x65\x6c\x6c\x6f"
        + b"\x90\xa2\x8a\x45"
        + b"\x48\x65\x6c\x6c\x6f"
        + KANJI_EXIT_KANJI_MODE
    )


def test_set_kanji_decoration() -> None:
    """should set kanji decoration."""
    instance = printer.Dummy()
    instance.set_kanji_decoration()
    assert instance.output == KANJI_PRINT_MODE + b"\x00" + KANJI_UNDERLINE + b"\x00"

    instance = printer.Dummy()
    instance.set_kanji_decoration(double_width=True, double_height=True, underline=1)
    assert instance.output == KANJI_PRINT_MODE + b"\x0C" + KANJI_UNDERLINE + b"\x01"


def test_define_user_defined_kanji() -> None:
    """should define user defined kanji."""
    instance = printer.Dummy()
    instance.define_user_defined_kanji(b"\x77\x7e", checkerboard_kanji)
    assert (
        instance.output == KANJI_DEFINE_USER_DEFINED + b"\x77\x7e" + checkerboard_kanji
    )


def test_delete_user_defined_kanji() -> None:
    """should delete user defined kanji."""
    instance = printer.Dummy()
    instance.delete_user_defined_kanji(b"\x77\x7e")
    assert instance.output == KANJI_DELETE_USER_DEFINED + b"\x77\x7e"


def test_kanji_set_encoding() -> None:
    """should set kanji encoding."""
    instance = printer.Dummy()
    instance.set_kanji_encoding("iso2022_jp")
    assert instance.output == KANJI_SET_ENCODING + b"\x00"

    instance = printer.Dummy()
    instance.set_kanji_encoding("shift_jis")
    assert instance.output == KANJI_SET_ENCODING + b"\x01"

    instance = printer.Dummy()
    instance.set_kanji_encoding("shift_jis_2004")
    assert instance.output == KANJI_SET_ENCODING + b"\x02"

    instance = printer.Dummy()
    instance.set_kanji_encoding("big5")
    assert instance.output == KANJI_SET_ENCODING + b"\x00"

    instance = printer.Dummy()
    instance.set_kanji_encoding("euc_kr")
    assert instance.output == KANJI_SET_ENCODING + b"\x00"

    instance = printer.Dummy()
    instance.set_kanji_encoding("gb2312")
    assert instance.output == KANJI_SET_ENCODING + b"\x00"

    instance = printer.Dummy()
    instance.set_kanji_encoding("gb18030")
    assert instance.output == KANJI_SET_ENCODING + b"\x00"


def test_kanji_spacing() -> None:
    """should set kanji spacing."""
    instance = printer.Dummy()
    instance.set_kanji_spacing(16, 0)
    assert instance.output == KANJI_SET_SPACING + b"\x10\x00"

    instance = printer.Dummy()
    instance.set_kanji_spacing(0, 16)
    assert instance.output == KANJI_SET_SPACING + b"\x00\x10"


def test_kanji_quadruple_size() -> None:
    """should set kanji quadruple size."""
    instance = printer.Dummy()
    instance.set_kanji_quadruple_size(True)
    assert instance.output == KANJI_SET_QUADRUPLE_SIZE + b"\x01"

    instance = printer.Dummy()
    instance.set_kanji_quadruple_size(False)
    assert instance.output == KANJI_SET_QUADRUPLE_SIZE + b"\x00"


def test_kanji_set_font() -> None:
    """should set kanji font."""
    instance = printer.Dummy()
    instance.set_kanji_font(0)
    assert instance.output == KANJI_SET_CHAR_STYLE + b"\x02\x00\x30\x00"

    instance = printer.Dummy()
    instance.set_kanji_font(1)
    assert instance.output == KANJI_SET_CHAR_STYLE + b"\x02\x00\x30\x01"

    instance = printer.Dummy()
    instance.set_kanji_font(2)
    assert instance.output == KANJI_SET_CHAR_STYLE + b"\x02\x00\x30\x02"
