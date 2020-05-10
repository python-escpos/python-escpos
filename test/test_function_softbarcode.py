#!/usr/bin/python

import escpos.printer as printer
import pytest


@pytest.fixture
def instance():
    return printer.Dummy()


def test_soft_barcode_ean8(instance):
    instance.soft_barcode("ean8", "1234")


def test_soft_barcode_ean8_nocenter(instance):
    instance.soft_barcode("ean8", "1234", center=False)
