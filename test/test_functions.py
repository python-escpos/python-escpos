from nose.tools import assert_raises
from escpos.printer import Dummy


def test_line_spacing_code_gen():
    printer = Dummy()
    printer.line_spacing(10)
    assert printer.output == '\x1b3\n'


def test_line_spacing_error_handling():
    printer = Dummy()
    with assert_raises(ValueError):
      printer.line_spacing(divisor=44)
    with assert_raises(ValueError):
      printer.line_spacing(divisor=80, spacing=86)
    with assert_raises(ValueError):
      printer.line_spacing(divisor=360, spacing=256)
    with assert_raises(ValueError):
      printer.line_spacing(divisor=180, spacing=256)