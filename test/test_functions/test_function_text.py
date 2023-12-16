#!/usr/bin/python
"""tests for the text printing function

:author: `Patrick Kanzler <dev@pkanzler.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import hypothesis.strategies as st
import mock
from hypothesis import given

from escpos.printer import Dummy


def get_printer() -> Dummy:
    return Dummy(magic_encode_args={"disabled": True, "encoding": "CP437"})


@given(text=st.text())
def test_text(text: str):
    """Test that text() calls the MagicEncode object."""
    instance = get_printer()
    with mock.patch.object(instance.magic, "write") as write:
        instance.text(text)
        write.assert_called_with(text)


def test_block_text() -> None:
    printer = get_printer()
    printer.block_text(
        "All the presidents men were eating falafel for breakfast.", font="a"
    )
    assert (
        printer.output == b"All the presidents men were eating falafel\nfor breakfast."
    )


def test_textln() -> None:
    printer = get_printer()
    printer.textln("hello, world")
    assert printer.output == b"hello, world\n"


def test_textln_empty() -> None:
    printer = get_printer()
    printer.textln()
    assert printer.output == b"\n"


def test_ln() -> None:
    printer = get_printer()
    printer.ln()
    assert printer.output == b"\n"


def test_multiple_ln() -> None:
    printer = get_printer()
    printer.ln(3)
    assert printer.output == b"\n\n\n"
