from escpos.printer import Dummy


def test_printer_dummy_clear() -> None:
    printer = Dummy()
    printer.text("Hello")
    printer.clear()
    assert printer.output == b""
