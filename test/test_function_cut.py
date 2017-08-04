from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six

import escpos.printer as printer
from escpos.constants import GS


def test_cut_without_feed():
    """Test cut without feeding paper"""
    instance = printer.Dummy()
    instance.cut(feed=False)
    expected = GS + b'V' + six.int2byte(66) + b'\x00'
    assert(instance.output == expected)
