#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the non-native part of qr()

:author: `Patrick Kanzler <dev@pkanzler.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2023 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import warnings

import mock
import pytest
from PIL import Image

from escpos.printer import Dummy


def test_image() -> None:
    """Test QR as image"""
    instance = Dummy()
    image_arguments = {
        "high_density_vertical": True,
        "high_density_horizontal": True,
        "impl": "bitImageRaster",
        "fragment_height": 960,
        "center": False,
    }
    instance.qr("1", native=False, image_arguments=image_arguments, size=1)
    print(instance.output)
    expected = (
        b"\x1bt\x00\n"
        b"\x1dv0\x00\x03\x00\x17\x00\x00\x00\x00\x7f\x1d\xfcAu\x04]\x1dt]et"
        b"]%tAI\x04\x7fU\xfc\x00 \x00}\xca\xa8h\xdf u\x95\x80x/ \x0b\xf4\x98\x00"
        b"T\x90\x7fzxA\x00\xd0]zp]o ]u\x80Ao(\x7fd\x90\x00\x00\x00"
        b"\n\n"
    )
    assert instance.output == expected


@mock.patch("escpos.printer.Dummy.image", spec=Dummy)
def test_type_of_object_passed_to_image_function(img_function):
    """
    Test the type of object that is passed to the image function during non-native qr-printing.

    The type should be PIL.Image
    """
    d = Dummy()
    d.qr("LoremIpsum")
    args, kwargs = img_function.call_args
    assert isinstance(args[0], Image.Image)


@mock.patch("escpos.printer.Dummy.image", spec=Dummy)
def test_parameter_image_arguments_passed_to_image_function(img_function):
    """Test the parameter passed to non-native qr printing."""
    d = Dummy()
    d.qr(
        "LoremIpsum",
        native=False,
        image_arguments={
            "impl": "bitImageColumn",
            "high_density_vertical": False,
            "center": True,
        },
    )
    args, kwargs = img_function.call_args
    assert "impl" in kwargs
    assert kwargs["impl"] == "bitImageColumn"
    assert "high_density_vertical" in kwargs
    assert kwargs["high_density_vertical"] is False
    assert "center" in kwargs
    assert kwargs["center"]


@pytest.fixture
def instance():
    return Dummy()


def test_center(instance):
    """Test printing qr codes."""
    instance.qr("LoremIpsum", center=True)


def test_deprecated_arguments(instance):
    """Test deprecation warning."""
    with warnings.catch_warnings(record=True) as w:
        # cause all warnings to always be triggered
        warnings.simplefilter("always")
        instance.qr(
            "LoremIpsum",
            impl="bitImageRaster",
            image_arguments={"impl": "bitImageColumn"},
        )
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated" in str(w[-1].message)
