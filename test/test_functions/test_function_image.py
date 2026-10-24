#!/usr/bin/env python
"""Image function tests- Check that image print commands are sent correctly.

:author: `Michael Billington <michael.billington@gmail.com>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `Michael Billington <michael.billington@gmail.com>`_
:license: MIT
"""

import pytest
from PIL import Image

import escpos.printer as printer
from escpos.exceptions import ImageWidthError


# Raster format print
def test_bit_image_black() -> None:
    """
    Test printing solid black bit image (raster)
    """
    instance = printer.Dummy()
    instance.image("test/resources/canvas_black.png", impl="bitImageRaster")
    assert instance.output == b"\x1dv0\x00\x01\x00\x01\x00\x80"
    # Same thing w/ object created on the fly, rather than a filename
    instance = printer.Dummy()
    im = Image.new("RGB", (1, 1), (0, 0, 0))
    instance.image(im, impl="bitImageRaster")
    assert instance.output == b"\x1dv0\x00\x01\x00\x01\x00\x80"


def test_bit_image_white() -> None:
    """
    Test printing solid white bit image (raster)
    """
    instance = printer.Dummy()
    instance.image("test/resources/canvas_white.png", impl="bitImageRaster")
    assert instance.output == b"\x1dv0\x00\x01\x00\x01\x00\x00"


def test_bit_image_both() -> None:
    """
    Test printing black/white bit image (raster)
    """
    instance = printer.Dummy()
    instance.image("test/resources/black_white.png", impl="bitImageRaster")
    assert instance.output == b"\x1dv0\x00\x01\x00\x02\x00\xc0\x00"


def test_bit_image_transparent() -> None:
    """
    Test printing black/transparent bit image (raster)
    """
    instance = printer.Dummy()
    instance.image("test/resources/black_transparent.png", impl="bitImageRaster")
    assert instance.output == b"\x1dv0\x00\x01\x00\x02\x00\xc0\x00"


# Column format print
def test_bit_image_colfmt_black() -> None:
    """
    Test printing solid black bit image (column format)
    """
    instance = printer.Dummy()
    instance.image("test/resources/canvas_black.png", impl="bitImageColumn")
    assert instance.output == b"\x1b3\x10\x1b*!\x01\x00\x80\x00\x00\x0a\x1b2"


def test_bit_image_colfmt_white() -> None:
    """
    Test printing solid white bit image (column format)
    """
    instance = printer.Dummy()
    instance.image("test/resources/canvas_white.png", impl="bitImageColumn")
    assert instance.output == b"\x1b3\x10\x1b*!\x01\x00\x00\x00\x00\x0a\x1b2"


def test_bit_image_colfmt_both() -> None:
    """
    Test printing black/white bit image (column format)
    """
    instance = printer.Dummy()
    instance.image("test/resources/black_white.png", impl="bitImageColumn")
    assert (
        instance.output == b"\x1b3\x10\x1b*!\x02\x00\x80\x00\x00\x80\x00\x00\x0a\x1b2"
    )


def test_bit_image_colfmt_transparent() -> None:
    """
    Test printing black/transparent bit image (column format)
    """
    instance = printer.Dummy()
    instance.image("test/resources/black_transparent.png", impl="bitImageColumn")
    assert (
        instance.output == b"\x1b3\x10\x1b*!\x02\x00\x80\x00\x00\x80\x00\x00\x0a\x1b2"
    )


# Graphics print
def test_graphics_black() -> None:
    """
    Test printing solid black graphics
    """
    instance = printer.Dummy()
    instance.image("test/resources/canvas_black.png", impl="graphics")
    assert (
        instance.output
        == b"\x1d(L\x0b\x000p0\x01\x011\x01\x00\x01\x00\x80\x1d(L\x02\x0002"
    )


def test_graphics_white() -> None:
    """
    Test printing solid white graphics
    """
    instance = printer.Dummy()
    instance.image("test/resources/canvas_white.png", impl="graphics")
    assert (
        instance.output
        == b"\x1d(L\x0b\x000p0\x01\x011\x01\x00\x01\x00\x00\x1d(L\x02\x0002"
    )


def test_graphics_both() -> None:
    """
    Test printing black/white graphics
    """
    instance = printer.Dummy()
    instance.image("test/resources/black_white.png", impl="graphics")
    assert (
        instance.output
        == b"\x1d(L\x0c\x000p0\x01\x011\x02\x00\x02\x00\xc0\x00\x1d(L\x02\x0002"
    )


def test_graphics_transparent() -> None:
    """
    Test printing black/transparent graphics
    """
    instance = printer.Dummy()
    instance.image("test/resources/black_transparent.png", impl="graphics")
    assert (
        instance.output
        == b"\x1d(L\x0c\x000p0\x01\x011\x02\x00\x02\x00\xc0\x00\x1d(L\x02\x0002"
    )


def test_large_graphics() -> None:
    """
    Test whether 'large' graphics that induce a fragmentation are handled correctly.
    """
    instance = printer.Dummy()
    instance.image(
        "test/resources/black_white.png", impl="bitImageRaster", fragment_height=1
    )
    assert (
        instance.output
        == b"\x1dv0\x00\x01\x00\x01\x00\xc0\x1dv0\x00\x01\x00\x01\x00\x00"
    )


@pytest.fixture
def dummy_with_width() -> printer.Dummy:
    instance = printer.Dummy()
    instance.profile.profile_data = {"media": {"width": {"pixels": 384}}}
    return instance


def test_width_too_large(dummy_with_width: printer.Dummy) -> None:
    """
    Test printing an image that is too large in width.
    """
    instance = dummy_with_width

    with pytest.raises(ImageWidthError):
        instance.image(Image.new("RGB", (385, 200)))

    instance.image(Image.new("RGB", (384, 200)))


def test_center_image(dummy_with_width: printer.Dummy) -> None:
    instance = dummy_with_width

    with pytest.raises(ImageWidthError):
        instance.image(Image.new("RGB", (385, 200)), center=True)

    instance.image(Image.new("RGB", (384, 200)), center=True)


def test_centered_image_split_preserves_centering() -> None:
    """Centering must survive fragmentation (issue #776).

    A tall centered image split into fragments must print identically to
    the same image pre-centered to the full media width.
    """
    black = Image.new("RGB", (10, 200), (0, 0, 0))
    reference = Image.new("RGB", (20, 200), (255, 255, 255))
    reference.paste(black, (5, 0))

    centered = printer.Dummy()
    centered.profile.profile_data = {"media": {"width": {"pixels": 20}}}
    centered.image(black, center=True, fragment_height=100)

    plain = printer.Dummy()
    plain.profile.profile_data = {"media": {"width": {"pixels": 20}}}
    plain.image(reference, fragment_height=100)

    assert centered.output == plain.output


@pytest.mark.parametrize("impl", ["bitImageRaster", "graphics", "bitImageColumn"])
@pytest.mark.parametrize("fragment_height", [100, 90])
def test_centered_split_matches_reference(impl: str, fragment_height: int) -> None:
    """Fragmented centering must match the reference for every renderer,
    including uneven splits (issue #776)."""
    black = Image.new("RGB", (10, 200), (0, 0, 0))
    reference = Image.new("RGB", (20, 200), (255, 255, 255))
    reference.paste(black, (5, 0))

    centered = printer.Dummy()
    centered.profile.profile_data = {"media": {"width": {"pixels": 20}}}
    centered.image(black, center=True, fragment_height=fragment_height, impl=impl)

    plain = printer.Dummy()
    plain.profile.profile_data = {"media": {"width": {"pixels": 20}}}
    plain.image(reference, fragment_height=fragment_height, impl=impl)

    assert centered.output != b""
    assert centered.output == plain.output


def test_oversize_fragmented_image_still_raises() -> None:
    """An over-wide tall image must raise before emitting output (issue #776)."""
    instance = printer.Dummy()
    instance.profile.profile_data = {"media": {"width": {"pixels": 20}}}

    with pytest.raises(ImageWidthError):
        instance.image(Image.new("RGB", (21, 200)), center=True, fragment_height=100)
    assert instance.output == b""


@pytest.mark.parametrize(
    "profile_data",
    [
        {"media": {"width": {"pixels": None}}},
        {"media": {"width": None}},
        {"media": None},
    ],
)
def test_none_width_falls_back_to_print_anyways(profile_data: dict) -> None:
    """A None media width must fall back to printing, not crash (issue #777)."""
    instance = printer.Dummy()
    instance.profile.profile_data = profile_data

    instance.image(Image.new("RGB", (10, 10)))
    assert instance.output != b""
    printed = len(instance.output)

    instance.image(Image.new("RGB", (10, 10)), center=True)
    assert len(instance.output) > printed


def test_none_width_tall_image_falls_back_to_print_anyways() -> None:
    """A None media width must not crash the fragmented path either (issue #777)."""
    instance = printer.Dummy()
    instance.profile.profile_data = {"media": {"width": None}}

    instance.image(Image.new("RGB", (10, 200)), fragment_height=100)
    assert instance.output != b""
