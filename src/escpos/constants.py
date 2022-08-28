#  -*- coding: utf-8 -*-
""" Set of ESC/POS Commands (Constants)

This module contains constants that are described in the esc/pos-documentation.
Since there is no definitive and unified specification for all esc/pos-like printers the constants could later be
moved to `capabilities` as in `escpos-php by @mike42 <https://github.com/mike42/escpos-php>`_.

:author: `Manuel F Martinez <manpaz@bashlinux.com>`_ and others
:organization: Bashlinux and `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2017 Bashlinux and python-escpos
:license: MIT
"""


import six

# Control characters
# as labelled in https://www.novopos.ch/client/EPSON/TM-T20/TM-T20_eng_qr.pdf
NUL = b"\x00"
EOT = b"\x04"
ENQ = b"\x05"
DLE = b"\x10"
DC4 = b"\x14"
CAN = b"\x18"
ESC = b"\x1b"
FS = b"\x1c"
GS = b"\x1d"

# Feed control sequences
CTL_LF = b"\n"  # Print and line feed
CTL_FF = b"\f"  # Form feed
CTL_CR = b"\r"  # Carriage return
CTL_HT = b"\t"  # Horizontal tab
CTL_SET_HT = ESC + b"\x44"  # Set horizontal tab positions
CTL_VT = b"\v"  # Vertical tab

# Printer hardware
HW_INIT = ESC + b"@"  # Clear data in buffer and reset modes
HW_SELECT = ESC + b"=\x01"  # Printer select

HW_RESET = ESC + b"\x3f\x0a\x00"  # Reset printer hardware
# (TODO: Where is this specified?)

# Cash Drawer (ESC p <pin> <on time: 2*ms> <off time: 2*ms>)
_CASH_DRAWER = (
    lambda m, t1="", t2="": ESC + b"p" + m + six.int2byte(t1) + six.int2byte(t2)
)
CD_KICK_DEC_SEQUENCE = (
    lambda esc, p, m, t1=50, t2=50: six.int2byte(esc)
    + six.int2byte(p)
    + six.int2byte(m)
    + six.int2byte(t1)
    + six.int2byte(t2)
)
CD_KICK_2 = _CASH_DRAWER(b"\x00", 50, 50)  # Sends a pulse to pin 2 []
CD_KICK_5 = _CASH_DRAWER(b"\x01", 50, 50)  # Sends a pulse to pin 5 []

# Paper Cutter
_CUT_PAPER = lambda m: GS + b"V" + m
PAPER_FULL_CUT = _CUT_PAPER(b"\x00")  # Full cut paper
PAPER_PART_CUT = _CUT_PAPER(b"\x01")  # Partial cut paper

# Beep (please note that the actual beep sequence may differ between devices)
BEEP = b"\x07"

# Panel buttons (e.g. the FEED button)
_PANEL_BUTTON = lambda n: ESC + b"c5" + six.int2byte(n)
PANEL_BUTTON_ON = _PANEL_BUTTON(0)  # enable all panel buttons
PANEL_BUTTON_OFF = _PANEL_BUTTON(1)  # disable all panel buttons

# Line display printing
LINE_DISPLAY_OPEN = ESC + b"\x3d\x02"
LINE_DISPLAY_CLEAR = ESC + b"\x40"
LINE_DISPLAY_CLOSE = ESC + b"\x3d\x01"

# Sheet modes
SHEET_SLIP_MODE = ESC + b"\x63\x30\x04"  # slip paper
SHEET_ROLL_MODE = ESC + b"\x63\x30\x01"  # paper roll

# Text format
# TODO: Acquire the "ESC/POS Application Programming Guide for Paper Roll
#       Printers" and tidy up this stuff too.
TXT_SIZE = GS + b"!"

TXT_NORMAL = ESC + b"!\x00"  # Normal text


TXT_STYLE = {
    "bold": {
        False: ESC + b"\x45\x00",  # Bold font OFF
        True: ESC + b"\x45\x01",  # Bold font ON
    },
    "underline": {
        0: ESC + b"\x2d\x00",  # Underline font OFF
        1: ESC + b"\x2d\x01",  # Underline font 1-dot ON
        2: ESC + b"\x2d\x02",  # Underline font 2-dot ON
    },
    "size": {
        "normal": TXT_NORMAL + ESC + b"!\x00",  # Normal text
        "2h": TXT_NORMAL + ESC + b"!\x10",  # Double height text
        "2w": TXT_NORMAL + ESC + b"!\x20",  # Double width text
        "2x": TXT_NORMAL + ESC + b"!\x30",  # Quad area text
    },
    "font": {
        "a": ESC + b"\x4d\x00",  # Font type A
        "b": ESC + b"\x4d\x00",  # Font type B
    },
    "align": {
        "left": ESC + b"\x61\x00",  # Left justification
        "center": ESC + b"\x61\x01",  # Centering
        "right": ESC + b"\x61\x02",  # Right justification
    },
    "invert": {
        True: GS + b"\x42\x01",  # Inverse Printing ON
        False: GS + b"\x42\x00",  # Inverse Printing OFF
    },
    "color": {
        "black": ESC + b"\x72\x00",  # Default Color
        "red": ESC + b"\x72\x01",  # Alternative Color, Usually Red
    },
    "flip": {True: ESC + b"\x7b\x01", False: ESC + b"\x7b\x00"},  # Flip ON  # Flip OFF
    "density": {
        0: GS + b"\x7c\x00",  # Printing Density -50%
        1: GS + b"\x7c\x01",  # Printing Density -37.5%
        2: GS + b"\x7c\x02",  # Printing Density -25%
        3: GS + b"\x7c\x03",  # Printing Density -12.5%
        4: GS + b"\x7c\x04",  # Printing Density  0%
        5: GS + b"\x7c\x08",  # Printing Density +50%
        6: GS + b"\x7c\x07",  # Printing Density +37.5%
        7: GS + b"\x7c\x06",  # Printing Density +25%
        8: GS + b"\x7c\x05",  # Printing Density +12.5%
    },
    "smooth": {
        True: GS + b"\x62\x01",  # Smooth ON
        False: GS + b"\x62\x00",  # Smooth OFF
    },
    "height": {  # Custom text height
        1: 0x00,
        2: 0x01,
        3: 0x02,
        4: 0x03,
        5: 0x04,
        6: 0x05,
        7: 0x06,
        8: 0x07,
    },
    "width": {  # Custom text width
        1: 0x00,
        2: 0x10,
        3: 0x20,
        4: 0x30,
        5: 0x40,
        6: 0x50,
        7: 0x60,
        8: 0x70,
    },
}

# Fonts
SET_FONT = lambda n: ESC + b"\x4d" + n
TXT_FONT_A = SET_FONT(b"\x00")  # Font type A
TXT_FONT_B = SET_FONT(b"\x01")  # Font type B

# Spacing
LINESPACING_RESET = ESC + b"2"
LINESPACING_FUNCS = {
    60: ESC + b"A",  # line_spacing/60 of an inch, 0 <= line_spacing <= 85
    360: ESC + b"+",  # line_spacing/360 of an inch, 0 <= line_spacing <= 255
    180: ESC + b"3",  # line_spacing/180 of an inch, 0 <= line_spacing <= 255
}

# Prefix to change the codepage. You need to attach a byte to indicate
# the codepage to use. We use escpos-printer-db as the data source.
CODEPAGE_CHANGE = ESC + b"\x74"

# Barcode format
_SET_BARCODE_TXT_POS = lambda n: GS + b"H" + n
BARCODE_TXT_OFF = _SET_BARCODE_TXT_POS(b"\x00")  # HRI barcode chars OFF
BARCODE_TXT_ABV = _SET_BARCODE_TXT_POS(b"\x01")  # HRI barcode chars above
BARCODE_TXT_BLW = _SET_BARCODE_TXT_POS(b"\x02")  # HRI barcode chars below
BARCODE_TXT_BTH = _SET_BARCODE_TXT_POS(b"\x03")  # HRI both above and below

_SET_HRI_FONT = lambda n: GS + b"f" + n
BARCODE_FONT_A = _SET_HRI_FONT(b"\x00")  # Font type A for HRI barcode chars
BARCODE_FONT_B = _SET_HRI_FONT(b"\x01")  # Font type B for HRI barcode chars

BARCODE_HEIGHT = GS + b"h"  # Barcode Height [1-255]
BARCODE_WIDTH = GS + b"w"  # Barcode Width  [2-6]

# NOTE: This isn't actually an ESC/POS command. It's the common prefix to the
#      two "print bar code" commands:
#      -  Type A: "GS k <type as integer> <data> NUL"
#      -  TYPE B: "GS k <type as letter> <data length> <data>"
#      The latter command supports more barcode types
_SET_BARCODE_TYPE = lambda m: GS + b"k" + six.int2byte(m)

# Barcodes for printing function type A
BARCODE_TYPE_A = {
    "UPC-A": _SET_BARCODE_TYPE(0),
    "UPC-E": _SET_BARCODE_TYPE(1),
    "EAN13": _SET_BARCODE_TYPE(2),
    "EAN8": _SET_BARCODE_TYPE(3),
    "CODE39": _SET_BARCODE_TYPE(4),
    "ITF": _SET_BARCODE_TYPE(5),
    "NW7": _SET_BARCODE_TYPE(6),
    "CODABAR": _SET_BARCODE_TYPE(6),  # Same as NW7
}

# Barcodes for printing function type B
# The first 8 are the same barcodes as type A
BARCODE_TYPE_B = {
    "UPC-A": _SET_BARCODE_TYPE(65),
    "UPC-E": _SET_BARCODE_TYPE(66),
    "EAN13": _SET_BARCODE_TYPE(67),
    "EAN8": _SET_BARCODE_TYPE(68),
    "CODE39": _SET_BARCODE_TYPE(69),
    "ITF": _SET_BARCODE_TYPE(70),
    "NW7": _SET_BARCODE_TYPE(71),
    "CODABAR": _SET_BARCODE_TYPE(71),  # Same as NW7
    "CODE93": _SET_BARCODE_TYPE(72),
    "CODE128": _SET_BARCODE_TYPE(73),
    "GS1-128": _SET_BARCODE_TYPE(74),
    "GS1 DATABAR OMNIDIRECTIONAL": _SET_BARCODE_TYPE(75),
    "GS1 DATABAR TRUNCATED": _SET_BARCODE_TYPE(76),
    "GS1 DATABAR LIMITED": _SET_BARCODE_TYPE(77),
    "GS1 DATABAR EXPANDED": _SET_BARCODE_TYPE(78),
}

BARCODE_FORMATS = {
    "UPC-A": ([(11, 12)], "^[0-9]{11,12}$"),
    "UPC-E": ([(7, 8), (11, 12)], "^([0-9]{7,8}|[0-9]{11,12})$"),
    "EAN13": ([(12, 13)], "^[0-9]{12,13}$"),
    "EAN8": ([(7, 8)], "^[0-9]{7,8}$"),
    "CODE39": ([(1, 255)], "^([0-9A-Z \$\%\+\-\.\/]+|\*[0-9A-Z \$\%\+\-\.\/]+\*)$"),
    "ITF": ([(2, 255)], "^([0-9]{2})+$"),
    "NW7": ([(1, 255)], "^[A-Da-d][0-9\$\+\-\.\/\:]+[A-Da-d]$"),
    "CODABAR": ([(1, 255)], "^[A-Da-d][0-9\$\+\-\.\/\:]+[A-Da-d]$"),  # Same as NW7
    "CODE93": ([(1, 255)], "^[\\x00-\\x7F]+$"),
    "CODE128": ([(2, 255)], "^\{[A-C][\\x00-\\x7F]+$"),
    "GS1-128": ([(2, 255)], "^\{[A-C][\\x00-\\x7F]+$"),  # same as CODE128
    "GS1 DATABAR OMNIDIRECTIONAL": ([(13, 13)], "^[0-9]{13}$"),
    "GS1 DATABAR TRUNCATED": ([(13, 13)], "^[0-9]{13}$"),  # same as GS1 omnidirectional
    "GS1 DATABAR LIMITED": ([(13, 13)], "^[01][0-9]{12}$"),
    "GS1 DATABAR EXPANDED": (
        [(2, 255)],
        "^\([0-9][A-Za-z0-9 \!\"\%\&'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\_\{]+$",
    ),
}

BARCODE_TYPES = {
    "A": BARCODE_TYPE_A,
    "B": BARCODE_TYPE_B,
}

# QRCode error correction levels
QR_ECLEVEL_L = 0
QR_ECLEVEL_M = 1
QR_ECLEVEL_Q = 2
QR_ECLEVEL_H = 3

# QRcode models
QR_MODEL_1 = 1
QR_MODEL_2 = 2
QR_MICRO = 3

# Image format
# NOTE: _PRINT_RASTER_IMG is the obsolete ESC/POS "print raster bit image"
#       command. The constants include a fragment of the data's header.
_PRINT_RASTER_IMG = lambda data: GS + b"v0" + data
S_RASTER_N = _PRINT_RASTER_IMG(b"\x00")  # Set raster image normal size
S_RASTER_2W = _PRINT_RASTER_IMG(b"\x01")  # Set raster image double width
S_RASTER_2H = _PRINT_RASTER_IMG(b"\x02")  # Set raster image double height
S_RASTER_Q = _PRINT_RASTER_IMG(b"\x03")  # Set raster image quadruple

# Status Command
RT_STATUS = DLE + EOT
RT_STATUS_ONLINE = RT_STATUS + b"\x01"
RT_STATUS_PAPER = RT_STATUS + b"\x04"
RT_MASK_ONLINE = 8
RT_MASK_PAPER = 18
RT_MASK_LOWPAPER = 30
RT_MASK_NOPAPER = 114
