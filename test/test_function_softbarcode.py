#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import escpos.printer as printer
import pytest


def test_soft_barcode():
    """just execute soft_barcode
    """
    instance = printer.Dummy()
    instance.soft_barcode("ean8", "1234")

