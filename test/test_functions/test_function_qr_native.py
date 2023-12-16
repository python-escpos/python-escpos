#!/usr/bin/python
"""test native QR code printing

:author: `Michael Billington <michael.billington@gmail.com>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2023 `Michael Billington <michael.billington@gmail.com>`_
:license: MIT
"""


import pytest

import escpos.printer as printer
from escpos.constants import QR_ECLEVEL_H, QR_MODEL_1


def test_defaults() -> None:
    """Test QR code with defaults"""
    instance = printer.Dummy()
    instance.qr("1234", native=True)
    expected = (
        b"\x1d(k\x04\x001A2\x00\x1d(k\x03\x001C\x03\x1d(k\x03\x001E0\x1d"
        b"(k\x07\x001P01234\x1d(k\x03\x001Q0"
    )
    assert instance.output == expected


def test_empty() -> None:
    """Test QR printing blank code"""
    instance = printer.Dummy()
    instance.qr("", native=True)
    assert instance.output == b""


def test_ec() -> None:
    """Test QR error correction setting"""
    instance = printer.Dummy()
    instance.qr("1234", native=True, ec=QR_ECLEVEL_H)
    expected = (
        b"\x1d(k\x04\x001A2\x00\x1d(k\x03\x001C\x03\x1d(k\x03\x001E3\x1d"
        b"(k\x07\x001P01234\x1d(k\x03\x001Q0"
    )
    assert instance.output == expected


def test_size() -> None:
    """Test QR box size"""
    instance = printer.Dummy()
    instance.qr("1234", native=True, size=7)
    expected = (
        b"\x1d(k\x04\x001A2\x00\x1d(k\x03\x001C\x07\x1d(k\x03\x001E0\x1d"
        b"(k\x07\x001P01234\x1d(k\x03\x001Q0"
    )
    assert instance.output == expected


def test_model() -> None:
    """Test QR model"""
    instance = printer.Dummy()
    instance.qr("1234", native=True, model=QR_MODEL_1)
    expected = (
        b"\x1d(k\x04\x001A1\x00\x1d(k\x03\x001C\x03\x1d(k\x03\x001E0\x1d"
        b"(k\x07\x001P01234\x1d(k\x03\x001Q0"
    )
    assert instance.output == expected


def test_invalid_ec() -> None:
    """Test invalid QR error correction"""
    instance = printer.Dummy()
    with pytest.raises(ValueError):
        instance.qr("1234", native=True, ec=-1)


def test_invalid_size() -> None:
    """Test invalid QR size"""
    instance = printer.Dummy()
    with pytest.raises(ValueError):
        instance.qr("1234", native=True, size=0)


def test_invalid_model() -> None:
    """Test invalid QR model"""
    instance = printer.Dummy()
    with pytest.raises(ValueError):
        instance.qr("1234", native=True, model="Hello")


def test_image_invalid_model() -> None:
    """Test unsupported QR model as image"""
    instance = printer.Dummy()
    with pytest.raises(ValueError):
        instance.qr("1234", native=False, model=QR_MODEL_1)


@pytest.fixture
def instance():
    return printer.Dummy()


def test_center_not_implementer(instance: printer.Dummy) -> None:
    with pytest.raises(NotImplementedError):
        instance.qr("test", center=True, native=True)
