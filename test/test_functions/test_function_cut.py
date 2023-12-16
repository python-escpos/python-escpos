import escpos.printer as printer
from escpos.constants import GS


def test_cut_without_feed() -> None:
    """Test cut without feeding paper"""
    instance = printer.Dummy()
    instance.cut(feed=False)
    expected = GS + b"V" + bytes((66,)) + b"\x00"
    assert instance.output == expected
