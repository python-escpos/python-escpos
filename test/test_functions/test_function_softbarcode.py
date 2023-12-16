#!/usr/bin/python

import barcode.errors
import pytest

import escpos.printer as printer


@pytest.fixture
def instance():
    return printer.Dummy()


def test_soft_barcode_ean8_invalid(instance: printer.Dummy) -> None:
    """test with an invalid barcode"""
    with pytest.raises(barcode.errors.BarcodeError):
        instance.barcode("1234", "ean8", force_software=True)


def test_soft_barcode_ean8(instance: printer.Dummy) -> None:
    """test with a valid ean8 barcode"""
    instance.barcode("1234567", "ean8", force_software=True)


def test_soft_barcode_ean8_nocenter(instance: printer.Dummy) -> None:
    instance.barcode("1234567", "ean8", align_ct=False, force_software=True)
