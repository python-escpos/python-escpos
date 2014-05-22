""" ESC/POS Commands (Constants) """

#{ Control characters
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

#{ Feed control sequences
CTL_LF = '\n'             # Print and line feed
CTL_FF = '\f'             # Form feed
CTL_CR = '\r'             # Carriage return
CTL_HT = '\t'             # Horizontal tab
CTL_VT = '\v'             # Vertical tab

#{ Printer hardware
HW_INIT   = ESC + '@'             # Clear data in buffer and reset modes
HW_SELECT = ESC + '=\x01'         # Printer select

HW_RESET  = ESC + '\x3f\x0a\x00'  # Reset printer hardware
                                  # (TODO: Where is this specified?)

#{ Cash Drawer (ESC p <pin> <on time: 2*ms> <off time: 2*ms>)
_CASH_DRAWER = lambda m, t1='', t2='': ESC + 'p' + m + t1 + t2
CD_KICK_2 = _CASH_DRAWER('\x00')  # Sends a pulse to pin 2 []
CD_KICK_5 = _CASH_DRAWER('\x01')  # Sends a pulse to pin 5 []

#{ Paper Cutter
_CUT_PAPER = lambda m: GS + 'V' + m
PAPER_FULL_CUT = _CUT_PAPER('\x00')  # Full cut paper
PAPER_PART_CUT = _CUT_PAPER('\x01')  # Partial cut paper

#{ Text format
# TODO: Acquire the "ESC/POS Application Programming Guide for Paper Roll
#       Printers" and tidy up this stuff too.
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

#{ Barcode format
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
#      -  "GS k <type as integer> <data> NUL"
#      -  "GS k <type as letter> <data length> <data>"
#      The latter command supports more barcode types
_SET_BARCODE_TYPE = lambda m: GS + 'k' + m
BARCODE_UPC_A  = _SET_BARCODE_TYPE('\x00')  # Barcode type UPC-A
BARCODE_UPC_E  = _SET_BARCODE_TYPE('\x01')  # Barcode type UPC-E
BARCODE_EAN13  = _SET_BARCODE_TYPE('\x02')  # Barcode type EAN13
BARCODE_EAN8   = _SET_BARCODE_TYPE('\x03')  # Barcode type EAN8
BARCODE_CODE39 = _SET_BARCODE_TYPE('\x04')  # Barcode type CODE39
BARCODE_ITF    = _SET_BARCODE_TYPE('\x05')  # Barcode type ITF
BARCODE_NW7    = _SET_BARCODE_TYPE('\x06')  # Barcode type NW7

#{ Image format
# NOTE: _PRINT_RASTER_IMG is the obsolete ESC/POS "print raster bit image"
#       command. The constants include a fragment of the data's header.
_PRINT_RASTER_IMG = lambda data: GS + 'v0' + data
S_RASTER_N  = _PRINT_RASTER_IMG('\x00')  # Set raster image normal size
S_RASTER_2W = _PRINT_RASTER_IMG('\x01')  # Set raster image double width
S_RASTER_2H = _PRINT_RASTER_IMG('\x02')  # Set raster image double height
S_RASTER_Q  = _PRINT_RASTER_IMG('\x03')  # Set raster image quadruple
