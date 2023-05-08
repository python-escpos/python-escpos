#!/usr/bin/python
"""test native QR code printing

:author: `Michael Billington <michael.billington@gmail.com>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `Michael Billington <michael.billington@gmail.com>`_
:license: MIT
"""


from nose.tools import raises
import pytest

import escpos.printer as printer
from escpos.constants import QR_ECLEVEL_H, QR_MODEL_1


def test_defaults():
    """Test QR code with defaults"""
    instance = printer.Dummy()
    instance.qr("1234", native=True)
    expected = (
        b"\x1d(k\x04\x001A2\x00\x1d(k\x03\x001C\x03\x1d(k\x03\x001E0\x1d"
        b"(k\x07\x001P01234\x1d(k\x03\x001Q0"
    )
    assert instance.output == expected


def test_empty():
    """Test QR printing blank code"""
    instance = printer.Dummy()
    instance.qr("", native=True)
    assert instance.output == b""


def test_ec():
    """Test QR error correction setting"""
    instance = printer.Dummy()
    instance.qr("1234", native=True, ec=QR_ECLEVEL_H)
    expected = (
        b"\x1d(k\x04\x001A2\x00\x1d(k\x03\x001C\x03\x1d(k\x03\x001E3\x1d"
        b"(k\x07\x001P01234\x1d(k\x03\x001Q0"
    )
    assert instance.output == expected


def test_size():
    """Test QR box size"""
    instance = printer.Dummy()
    instance.qr("1234", native=True, size=7)
    expected = (
        b"\x1d(k\x04\x001A2\x00\x1d(k\x03\x001C\x07\x1d(k\x03\x001E0\x1d"
        b"(k\x07\x001P01234\x1d(k\x03\x001Q0"
    )
    assert instance.output == expected


def test_model():
    """Test QR model"""
    instance = printer.Dummy()
    instance.qr("1234", native=True, model=QR_MODEL_1)
    expected = (
        b"\x1d(k\x04\x001A1\x00\x1d(k\x03\x001C\x03\x1d(k\x03\x001E0\x1d"
        b"(k\x07\x001P01234\x1d(k\x03\x001Q0"
    )
    assert instance.output == expected


@raises(ValueError)
def test_invalid_ec():
    """Test invalid QR error correction"""
    instance = printer.Dummy()
    instance.qr("1234", native=True, ec=-1)


@raises(ValueError)
def test_invalid_size():
    """Test invalid QR size"""
    instance = printer.Dummy()
    instance.qr("1234", native=True, size=0)


@raises(ValueError)
def test_invalid_model():
    """Test invalid QR model"""
    instance = printer.Dummy()
    instance.qr("1234", native=True, model="Hello")


@pytest.mark.skip("this test has to be debugged")
def test_image():
    """Test QR as image"""
    instance = printer.Dummy()
    instance.qr("1", native=False, size=1)
    print(instance.output)
    expected = (
        b"\x1bt\x00\n"
        b"\x1dv0\x00\x03\x00\x17\x00\x00\x00\x00\x7f]\xfcA\x19\x04]it]et"
        b"]ItA=\x04\x7fU\xfc\x00\x0c\x00y~t4\x7f =\xa84j\xd9\xf0\x05\xd4\x90\x00"
        b"i(\x7f<\xa8A \xd8]'\xc4]y\xf8]E\x80Ar\x94\x7fR@\x00\x00\x00"
        b"\n\n"
    )
    assert instance.output == expected


@raises(ValueError)
def test_image_invalid_model():
    """Test unsupported QR model as image"""
    instance = printer.Dummy()
    instance.qr("1234", native=False, model=QR_MODEL_1)


@pytest.fixture
def instance():
    return printer.Dummy()


def test_center_not_implementer(instance):
    with pytest.raises(NotImplementedError):
        instance.qr("test", center=True, native=True)
