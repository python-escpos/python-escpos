#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the non-native part of qr()

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import pytest
import mock

from escpos.printer import Dummy
from PIL import Image


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


@pytest.fixture
def instance():
    return Dummy()


def test_center(instance):
    instance.qr("LoremIpsum", center=True)
