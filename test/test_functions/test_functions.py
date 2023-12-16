import pytest

from escpos.printer import Dummy


def test_line_spacing_code_gen() -> None:
    printer = Dummy()
    printer.line_spacing(10)
    assert printer.output == b"\x1b3\n"


def test_line_spacing_rest() -> None:
    printer = Dummy()
    printer.line_spacing()
    assert printer.output == b"\x1b2"


def test_line_spacing_error_handling() -> None:
    printer = Dummy()
    with pytest.raises(ValueError):
        printer.line_spacing(99, divisor=44)
    with pytest.raises(ValueError):
        printer.line_spacing(divisor=80, spacing=86)
    with pytest.raises(ValueError):
        printer.line_spacing(divisor=360, spacing=256)
    with pytest.raises(ValueError):
        printer.line_spacing(divisor=180, spacing=256)
