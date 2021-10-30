import six

import escpos.printer as printer
from escpos.constants import GS


def test_cut_without_feed():
    """Test cut without feeding paper"""
    instance = printer.Dummy()
    instance.cut(feed=False)
    expected = GS + b"V" + six.int2byte(66) + b"\x00"
    assert instance.output == expected
