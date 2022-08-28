#!/usr/bin/python

import escpos.printer as printer
import barcode.errors
import pytest


@pytest.fixture
def instance():
    return printer.Dummy()


def test_soft_barcode_ean8_invalid(instance):
    """test with an invalid barcode"""
    with pytest.raises(barcode.errors.BarcodeError):
        instance.soft_barcode("ean8", "1234")


def test_soft_barcode_ean8(instance):
    """test with a valid ean8 barcode"""
    instance.soft_barcode("ean8", "1234567")


def test_soft_barcode_ean8_nocenter(instance):
    instance.soft_barcode("ean8", "1234567", center=False)
