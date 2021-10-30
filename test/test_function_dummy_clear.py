from nose.tools import assert_raises
from escpos.printer import Dummy


def test_printer_dummy_clear():
    printer = Dummy()
    printer.text("Hello")
    printer.clear()
    assert printer.output == b""
