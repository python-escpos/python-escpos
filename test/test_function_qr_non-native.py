#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the non-native part of qr()

:author: `Patrick Kanzler <dev@pkanzler.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import warnings

import mock
import pytest
from PIL import Image

from escpos.printer import Dummy


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
