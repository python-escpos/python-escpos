#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""A simple command-line interface for common python-escpos functionality

Usage: python -m escpos.cli --help

Dependencies:
- DavisGoglin/python-escpos or better
- A file named weather.png (for the 'test' subcommand)

Reasons for using the DavisGoglin/python-escpos fork:
- image() accepts a PIL.Image object rather than requiring me to choose
  between writing a temporary file to disk or calling a "private" method.
- fullimage() allows me to print images of arbitrary length using slicing.

How to print unsupported barcodes:
    barcode -b 'BARCODE' -e 'code39' -E | convert -density 200% eps:- code.png
    python test_escpos.py --images code.png

Copyright (C) 2014 Stephan Sokolow (deitarion/SSokolow)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import absolute_import

__author__ = "Stephan Sokolow (deitarion/SSokolow)"
__license__ = "MIT"

import re

from escpos import printer

epson = printer.Usb(0x0416, 0x5011)
# TODO: Un-hardcode this


def _print_text_file(path):
    """Print the given text file"""
    epson.set(align='left')
    with open(path, 'rU') as fobj:
        for line in fobj:
            epson.text(line)


def _print_image_file(path):
    """Print the given image file."""
    epson.fullimage(path, histeq=False, width=384)


def print_files(args):
    """The 'print' subcommand"""
    for path in args.paths:
        if args.images:
            _print_image_file(path)
        else:
            _print_text_file(path)
    epson.cut()

# {{{ 'echo' Subcommand

KNOWN_BARCODE_TYPES = ['UPC-A', 'UPC-E', 'EAN13', 'ITF']
re_barcode_escape = re.compile(r'^%(?P<type>\S+)\s(?P<data>[0-9X]+)$')


def echo(args):  # pylint: disable=unused-argument
    """TTY-like line-by-line keyboard-to-printer echo loop."""
    try:
        while True:
            line = raw_input()
            match = re_barcode_escape.match(line)
            if match and match.group('type') in KNOWN_BARCODE_TYPES:
                bctype, data = match.groups()
                epson.barcode(data, bctype, 48, 2, '', '')
                epson.set(align='left')
            else:
                epson.text('{0}\n'.format(line))
    except KeyboardInterrupt:
        epson.cut()

# }}}
# {{{ 'test' Subcommand

from PIL import Image, ImageDraw


def _stall_test(width, height):
    """Generate a pattern to detect print glitches due to vertical stalling."""
    img = Image.new('1', (width, height))
    for pos in [(x, y) for y in range(0, height) for x in range(0, width)]:
        img.putpixel(pos, not sum(pos) % 10)
    return img


def _test_basic():
    """The original test code from python-escpos's Usage wiki page"""
    epson.set(align='left')
    # Print text
    epson.text("TODO:\n")  # pylint: disable=fixme
    epson.text("[ ] Task 1\n")
    epson.text("[ ] Task 2\n")
    # Print image
    # TODO: Bundle an image so this can be used
    # epson.image("weather.png")
    # Print QR Code (must have a white border to be scanned)
    epson.set(align='center')
    epson.text("Scan to recall TODO list")  # pylint: disable=fixme
    epson.qr("http://www.example.com/")
    # Print barcode
    epson.barcode('1234567890128', 'EAN13', 32, 2, '', '')
    # Cut paper
    epson.cut()


def _test_barcodes():
    """Print test barcodes for all ESCPOS-specified formats."""
    for name, data in (
            # pylint: disable=bad-continuation
            ('UPC-A', '123456789012\x00'),
            ('UPC-E', '02345036\x00'),
            ('EAN13', '1234567890128\x00'),
            ('EAN8', '12345670\x00'),
            ('CODE39', 'BARCODE12345678\x00'),
            ('ITF', '123456\x00'),
            ('CODABAR', 'A40156B'),
            # TODO: CODE93 and CODE128
    ):
        # TODO: Fix the library to restore old alignment somehow
        epson.set(align='center')
        epson.text('\n{0}\n'.format(name))
        epson.barcode(data, name, 64, 2, '', '')


def _test_patterns(width=384, height=255):
    """Print a set of test patterns for raster image output."""
    # Test our guess of the paper width
    img = Image.new('1', (width, height), color=1)
    draw = ImageDraw.Draw(img)
    draw.polygon(((0, 0), img.size, (0, img.size[1])), fill=0)
    epson.image(img)
    del draw, img

    # Test the consistency of printing large data and whether stall rate is
    # affected by data rate
    epson.image(_stall_test(width, height))
    epson.image(_stall_test(width / 2, height))


def test(args):
    """The 'test' subcommand"""
    if args.barcodes:
        _test_barcodes()
    elif args.patterns:
        _test_patterns()
    else:
        _test_basic()


# }}}

def main():
    """Wrapped in a function for import and entry point compatibility"""
    # pylint: disable=bad-continuation

    import argparse

    parser = argparse.ArgumentParser(
        description="Command-line interface to python-escpos")
    subparsers = parser.add_subparsers(title='subcommands')

    echo_parser = subparsers.add_parser('echo', help='Echo the keyboard to '
                                                     'the printer line-by-line (Exit with Ctrl+C)')
    echo_parser.set_defaults(func=echo)

    print_parser = subparsers.add_parser('print', help='Print the given files')
    print_parser.add_argument('--images', action='store_true',
                              help="Provided files are images rather than text files.")
    print_parser.add_argument('paths', metavar='path', nargs='+')
    print_parser.set_defaults(func=print_files)

    test_parser = subparsers.add_parser('test', help='Print test patterns')
    test_modes = test_parser.add_mutually_exclusive_group()
    test_modes.add_argument('--barcodes', action='store_true',
                            help="Test supported barcode types (Warning: Some printers must be "
                                 "reset after attempting an unsupported barcode type.)")
    test_modes.add_argument('--patterns', action='store_true',
                            help="Print test patterns")
    test_parser.set_defaults(func=test)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()

# vim: set sw=4 sts=4 :
