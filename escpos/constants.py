""" Set of ESC/POS Commands (Constants)

This module contains constants that are described in the esc/pos-documentation.
Since there is no definitive and unified specification for all esc/pos-like printers the constants could later be
moved to `capabilities` as in `escpos-php by @mike42 <https://github.com/mike42/escpos-php>`_.

:author: `Manuel F Martinez <manpaz@bashlinux.com>`_ and others
:organization: Bashlinux and `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012 Bashlinux
:license: GNU GPL v3
"""

# Control characters
# as labelled in http://www.novopos.ch/client/EPSON/TM-T20/TM-T20_eng_qr.pdf
NUL = '\x00'
EOT = '\x04'
ENQ = '\x05'
DLE = '\x10'
DC4 = '\x14'
CAN = '\x18'
ESC = '\x1b'
FS  = '\x1c'
GS  = '\x1d'

# Feed control sequences
CTL_LF = '\n'             # Print and line feed
CTL_FF = '\f'             # Form feed
CTL_CR = '\r'             # Carriage return
CTL_HT = '\t'             # Horizontal tab
CTL_SET_HT = ESC + '\x44' # Set horizontal tab positions
CTL_VT = '\v'             # Vertical tab

# Printer hardware
HW_INIT   = ESC + '@'             # Clear data in buffer and reset modes
HW_SELECT = ESC + '=\x01'         # Printer select

HW_RESET  = ESC + '\x3f\x0a\x00'  # Reset printer hardware
                                  # (TODO: Where is this specified?)

#{ Cash Drawer (ESC p <pin> <on time: 2*ms> <off time: 2*ms>)
_CASH_DRAWER = lambda m, t1='', t2='': ESC + 'p' + m + chr(t1) + chr(t2)
CD_KICK_2 = _CASH_DRAWER('\x00', 50, 50)  # Sends a pulse to pin 2 []
CD_KICK_5 = _CASH_DRAWER('\x01', 50, 50)  # Sends a pulse to pin 5 []

# Paper Cutter
_CUT_PAPER = lambda m: GS + 'V' + m
PAPER_FULL_CUT = _CUT_PAPER('\x00')  # Full cut paper
PAPER_PART_CUT = _CUT_PAPER('\x01')  # Partial cut paper

# Text format
# TODO: Acquire the "ESC/POS Application Programming Guide for Paper Roll
#       Printers" and tidy up this stuff too.
TXT_FLIP_ON    = ESC + '\x7b\x01'
TXT_FLIP_OFF   = ESC + '\x7b\x00'
TXT_SMOOTH_ON  = GS + '\x62\x01'
TXT_SMOOTH_OFF = GS + '\x62\x00'
TXT_SIZE       = GS + '!'
TXT_WIDTH      = {1: 0x00,
                  2: 0x10,
                  3: 0x20,
                  4: 0x30,
                  5: 0x40,
                  6: 0x50,
                  7: 0x60,
                  8: 0x70}
TXT_HEIGHT     = {1: 0x00,
                  2: 0x01,
                  3: 0x02,
                  4: 0x03,
                  5: 0x04,
                  6: 0x05,
                  7: 0x06,
                  8: 0x07}
TXT_NORMAL     = ESC + '!\x00'     # Normal text
TXT_2HEIGHT    = ESC + '!\x10'     # Double height text
TXT_2WIDTH     = ESC + '!\x20'     # Double width text
TXT_4SQUARE    = ESC + '!\x30'     # Quad area text
TXT_UNDERL_OFF = ESC + '\x2d\x00'  # Underline font OFF
TXT_UNDERL_ON  = ESC + '\x2d\x01'  # Underline font 1-dot ON
TXT_UNDERL2_ON = ESC + '\x2d\x02'  # Underline font 2-dot ON
TXT_BOLD_OFF   = ESC + '\x45\x00'  # Bold font OFF
TXT_BOLD_ON    = ESC + '\x45\x01'  # Bold font ON
TXT_FONT_A     = ESC + '\x4d\x00'  # Font type A
TXT_FONT_B     = ESC + '\x4d\x01'  # Font type B
TXT_ALIGN_LT   = ESC + '\x61\x00'  # Left justification
TXT_ALIGN_CT   = ESC + '\x61\x01'  # Centering
TXT_ALIGN_RT   = ESC + '\x61\x02'  # Right justification
TXT_INVERT_ON  = GS  + '\x42\x01'  # Inverse Printing ON
TXT_INVERT_OFF = GS  + '\x42\x00'  # Inverse Printing OFF

# Char code table
CHARCODE_PC437  = ESC + '\x74\x00'  # USA: Standard Europe
CHARCODE_JIS    = ESC + '\x74\x01'  # Japanese Katakana
CHARCODE_PC850  = ESC + '\x74\x02'  # Multilingual
CHARCODE_PC860  = ESC + '\x74\x03'  # Portuguese
CHARCODE_PC863  = ESC + '\x74\x04'  # Canadian-French
CHARCODE_PC865  = ESC + '\x74\x05'  # Nordic
CHARCODE_WEU    = ESC + '\x74\x06'  # Simplified Kanji, Hirakana
CHARCODE_GREEK  = ESC + '\x74\x07'  # Simplified Kanji
CHARCODE_HEBREW = ESC + '\x74\x08'  # Simplified Kanji
CHARCODE_PC1252 = ESC + '\x74\x11'  # Western European Windows Code Set
CHARCODE_PC866  = ESC + '\x74\x12'  # Cirillic #2
CHARCODE_PC852  = ESC + '\x74\x13'  # Latin 2
CHARCODE_PC858  = ESC + '\x74\x14'  # Euro
CHARCODE_THAI42 = ESC + '\x74\x15'  # Thai character code 42
CHARCODE_THAI11 = ESC + '\x74\x16'  # Thai character code 11
CHARCODE_THAI13 = ESC + '\x74\x17'  # Thai character code 13
CHARCODE_THAI14 = ESC + '\x74\x18'  # Thai character code 14
CHARCODE_THAI16 = ESC + '\x74\x19'  # Thai character code 16
CHARCODE_THAI17 = ESC + '\x74\x1a'  # Thai character code 17
CHARCODE_THAI18 = ESC + '\x74\x1b'  # Thai character code 18

# Barcode format
_SET_BARCODE_TXT_POS = lambda n: GS + 'H' + n
BARCODE_TXT_OFF = _SET_BARCODE_TXT_POS('\x00')  # HRI barcode chars OFF
BARCODE_TXT_ABV = _SET_BARCODE_TXT_POS('\x01')  # HRI barcode chars above
BARCODE_TXT_BLW = _SET_BARCODE_TXT_POS('\x02')  # HRI barcode chars below
BARCODE_TXT_BTH = _SET_BARCODE_TXT_POS('\x03')  # HRI both above and below

_SET_HRI_FONT = lambda n: GS + 'f' + n
BARCODE_FONT_A = _SET_HRI_FONT('\x00')  # Font type A for HRI barcode chars
BARCODE_FONT_B = _SET_HRI_FONT('\x01')  # Font type B for HRI barcode chars

BARCODE_HEIGHT = GS + 'h'  # Barcode Height [1-255]
BARCODE_WIDTH  = GS + 'w'  # Barcode Width  [2-6]

#NOTE: This isn't actually an ESC/POS command. It's the common prefix to the
#      two "print bar code" commands:
#      -  Type A: "GS k <type as integer> <data> NUL"
#      -  TYPE B: "GS k <type as letter> <data length> <data>"
#      The latter command supports more barcode types
_SET_BARCODE_TYPE = lambda m: GS + 'k' + m

# Barcodes for type A
BARCODE_A_UPC_A  = _SET_BARCODE_TYPE(chr(0))  # Barcode type UPC-A
BARCODE_A_UPC_E  = _SET_BARCODE_TYPE(chr(1))  # Barcode type UPC-E
BARCODE_A_EAN13  = _SET_BARCODE_TYPE(chr(2))  # Barcode type EAN13
BARCODE_A_EAN8   = _SET_BARCODE_TYPE(chr(3))  # Barcode type EAN8
BARCODE_A_CODE39 = _SET_BARCODE_TYPE(chr(4))  # Barcode type CODE39
BARCODE_A_ITF    = _SET_BARCODE_TYPE(chr(5))  # Barcode type ITF
BARCODE_A_NW7    = _SET_BARCODE_TYPE(chr(6))  # Barcode type NW7

# Barcodes for type B
BARCODE_B_UPC_A             = _SET_BARCODE_TYPE(chr(65))  # Barcode type UPC-A
BARCODE_B_UPC_E             = _SET_BARCODE_TYPE(chr(66))  # Barcode type UPC-E
BARCODE_B_EAN13             = _SET_BARCODE_TYPE(chr(67))  # Barcode type EAN13
BARCODE_B_EAN8              = _SET_BARCODE_TYPE(chr(68))  # Barcode type EAN8
BARCODE_B_CODE39            = _SET_BARCODE_TYPE(chr(69))  # Barcode type CODE39
BARCODE_B_ITF               = _SET_BARCODE_TYPE(chr(70))  # Barcode type ITF
BARCODE_B_NW7               = _SET_BARCODE_TYPE(chr(71))  # Barcode type NW7
BARCODE_B_CODE93            = _SET_BARCODE_TYPE(chr(72))  # Barcode type CODE93
BARCODE_B_CODE128           = _SET_BARCODE_TYPE(chr(73))  # Barcode type CODE128
BARCODE_B_GS1_128           = _SET_BARCODE_TYPE(chr(74))  # Barcode type GS1_128
BARCODE_B_GS1_DATABAR_OMNI  = _SET_BARCODE_TYPE(chr(75))  # Barcode type GS1 DataBar Omnidirectional
BARCODE_B_GS1_DATABAR_TRUNC = _SET_BARCODE_TYPE(chr(76))  # Barcode type GS1 DataBar Truncated
BARCODE_B_GS1_DATABAR_LIM   = _SET_BARCODE_TYPE(chr(77))  # Barcode type GS1 DataBar Limited
BARCODE_B_GS1_DATABAR_EXP   = _SET_BARCODE_TYPE(chr(78))  # Barcode type GS1 DataBar Expanded

# Constants to be used when the user is calling the function. All uppercase.
BARCODE_TYPE_A = {
    'UPC-A': BARCODE_A_UPC_A,
    'UPC-E': BARCODE_A_UPC_E,
    'EAN13': BARCODE_A_EAN13,
    'EAN8': BARCODE_A_EAN8,
    'CODE39': BARCODE_A_CODE39,
    'ITF': BARCODE_A_ITF,
    'NW7': BARCODE_A_NW7,
    'CODABAR': BARCODE_A_NW7,
}

BARCODE_TYPE_B = {
    'UPC-A': BARCODE_B_UPC_A,
    'UPC-E': BARCODE_B_UPC_E,
    'EAN13': BARCODE_B_EAN13,
    'EAN8': BARCODE_B_EAN8,
    'CODE39': BARCODE_B_CODE39,
    'ITF': BARCODE_B_ITF,
    'NW7': BARCODE_B_NW7,
    'CODABAR': BARCODE_B_NW7,
    'CODE93': BARCODE_B_CODE93,
    'CODE128': BARCODE_B_CODE128,
    'GS1_128': BARCODE_B_GS1_128,
    'GS1 DATABAR OMNIDIRECTIONAL': BARCODE_B_GS1_DATABAR_OMNI,
    'GS1 DATABAR TRUNCATED': BARCODE_B_GS1_DATABAR_TRUNC,
    'GS1 DATABAR LIMITED': BARCODE_B_GS1_DATABAR_LIM,
    'GS1 DATABAR EXPANDED': BARCODE_B_GS1_DATABAR_EXP,
}

BARCODE_TYPES = {
    'A': BARCODE_TYPE_A,
    'B': BARCODE_TYPE_B,
}


# Image format
# NOTE: _PRINT_RASTER_IMG is the obsolete ESC/POS "print raster bit image"
#       command. The constants include a fragment of the data's header.
_PRINT_RASTER_IMG = lambda data: GS + 'v0' + data
S_RASTER_N  = _PRINT_RASTER_IMG('\x00')  # Set raster image normal size
S_RASTER_2W = _PRINT_RASTER_IMG('\x01')  # Set raster image double width
S_RASTER_2H = _PRINT_RASTER_IMG('\x02')  # Set raster image double height
S_RASTER_Q  = _PRINT_RASTER_IMG('\x03')  # Set raster image quadruple

# Printing Density
PD_N50          = GS + '\x7c\x00'  # Printing Density -50%
PD_N37          = GS + '\x7c\x01'  # Printing Density -37.5%
PD_N25          = GS + '\x7c\x02'  # Printing Density -25%
PD_N12          = GS + '\x7c\x03'  # Printing Density -12.5%
PD_0            = GS + '\x7c\x04'  # Printing Density  0%
PD_P50          = GS + '\x7c\x08'  # Printing Density +50%
PD_P37          = GS + '\x7c\x07'  # Printing Density +37.5%
PD_P25          = GS + '\x7c\x06'  # Printing Density +25%
PD_P12          = GS + '\x7c\x05'  # Printing Density +12.5%
