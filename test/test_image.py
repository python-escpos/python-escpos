#!/usr/bin/env python
""" Image tests- Check that images from different source formats are correctly
converted to ESC/POS column & raster formats.

:author: `Michael Billington <michael.billington@gmail.com>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `Michael Billington <michael.billington@gmail.com>`_
:license: MIT
"""

from escpos.image import EscposImage


def test_image_black():
    """
    Test rendering solid black image
    """
    for img_format in ["png", "jpg", "gif"]:
        _load_and_check_img("canvas_black." + img_format, 1, 1, b"\x80", [b"\x80"])


def test_image_black_transparent():
    """
    Test rendering black/transparent image
    """
    for img_format in ["png", "gif"]:
        _load_and_check_img(
            "black_transparent." + img_format, 2, 2, b"\xc0\x00", [b"\x80\x80"]
        )


def test_image_black_white():
    """
    Test rendering black/white image
    """
    for img_format in ["png", "jpg", "gif"]:
        _load_and_check_img(
            "black_white." + img_format, 2, 2, b"\xc0\x00", [b"\x80\x80"]
        )


def test_image_white():
    """
    Test rendering solid white image
    """
    for img_format in ["png", "jpg", "gif"]:
        _load_and_check_img("canvas_white." + img_format, 1, 1, b"\x00", [b"\x00"])


def test_split():
    """
    test whether the split-function works as expected
    """
    im = EscposImage("test/resources/black_white.png")
    (upper_part, lower_part) = im.split(1)
    upper_part = EscposImage(upper_part)
    lower_part = EscposImage(lower_part)
    assert upper_part.width == lower_part.width == 2
    assert upper_part.height == lower_part.height == 1
    assert upper_part.to_raster_format() == b"\xc0"
    assert lower_part.to_raster_format() == b"\x00"


def _load_and_check_img(
    filename,
    width_expected,
    height_expected,
    raster_format_expected,
    column_format_expected,
):
    """
    Load an image, and test whether raster & column formatted output, sizes, etc match expectations.
    """
    im = EscposImage("test/resources/" + filename)
    assert im.width == width_expected
    assert im.height == height_expected
    assert im.to_raster_format() == raster_format_expected
    i = 0
    for row in im.to_column_format(False):
        assert row == column_format_expected[i]
        i += 1
