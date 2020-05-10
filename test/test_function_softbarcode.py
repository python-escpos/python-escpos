#!/usr/bin/python

import escpos.printer as printer
import pytest


def test_soft_barcode():
    """just execute soft_barcode
    """
    instance = printer.Dummy()
    instance.soft_barcode("ean8", "1234")

