""" ESC/POS Commands (Constants) """

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
CTL_LF     = '\x0a'               # Print and line feed
CTL_FF     = '\x0c'               # Form feed
CTL_CR     = '\x0d'               # Carriage return
CTL_HT     = '\x09'               # Horizontal tab
CTL_SET_HT = ESC + '\x44'           # Set horizontal tab positions
CTL_VT     = ESC + '\x64\x04'       # Vertical tab
# Printer hardware
HW_INIT    = ESC + '\x40'           # Clear data in buffer and reset modes
HW_SELECT  = ESC + '\x3d\x01'       # Printer select
HW_RESET   = ESC + '\x3f\x0a\x00'   # Reset printer hardware
# Cash Drawer
CD_KICK_2  = ESC + '\x70\x00'       # Sends a pulse to pin 2 []
CD_KICK_5  = ESC + '\x70\x01'       # Sends a pulse to pin 5 []
# Paper
PAPER_FULL_CUT  = GS + '\x56\x00'  # Full cut paper
PAPER_PART_CUT  = GS + '\x56\x01'  # Partial cut paper
# Text format
TXT_NORMAL      = ESC + '\x21\x00'  # Normal text
TXT_2HEIGHT     = ESC + '\x21\x10'  # Double height text
TXT_2WIDTH      = ESC + '\x21\x20'  # Double width text
TXT_4SQUARE     = ESC + '\x21\x30'  # Quad area text
TXT_UNDERL_OFF  = ESC + '\x2d\x00'  # Underline font OFF
TXT_UNDERL_ON   = ESC + '\x2d\x01'  # Underline font 1-dot ON
TXT_UNDERL2_ON  = ESC + '\x2d\x02'  # Underline font 2-dot ON
TXT_BOLD_OFF    = ESC + '\x45\x00'  # Bold font OFF
TXT_BOLD_ON     = ESC + '\x45\x01'  # Bold font ON
TXT_FONT_A      = ESC + '\x4d\x00'  # Font type A
TXT_FONT_B      = ESC + '\x4d\x01'  # Font type B
TXT_ALIGN_LT    = ESC + '\x61\x00'  # Left justification
TXT_ALIGN_CT    = ESC + '\x61\x01'  # Centering
TXT_ALIGN_RT    = ESC + '\x61\x02'  # Right justification
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
BARCODE_TXT_OFF = GS + '\x48\x00'  # HRI barcode chars OFF
BARCODE_TXT_ABV = GS + '\x48\x01'  # HRI barcode chars above
BARCODE_TXT_BLW = GS + '\x48\x02'  # HRI barcode chars below
BARCODE_TXT_BTH = GS + '\x48\x03'  # HRI barcode chars both above and below
BARCODE_FONT_A  = GS + '\x66\x00'  # Font type A for HRI barcode chars
BARCODE_FONT_B  = GS + '\x66\x01'  # Font type B for HRI barcode chars
BARCODE_HEIGHT  = GS + '\x68\x64'  # Barcode Height [1-255]
BARCODE_WIDTH   = GS + '\x77\x03'  # Barcode Width  [2-6]
BARCODE_UPC_A   = GS + '\x6b\x00'  # Barcode type UPC-A
BARCODE_UPC_E   = GS + '\x6b\x01'  # Barcode type UPC-E
BARCODE_EAN13   = GS + '\x6b\x02'  # Barcode type EAN13
BARCODE_EAN8    = GS + '\x6b\x03'  # Barcode type EAN8
BARCODE_CODE39  = GS + '\x6b\x04'  # Barcode type CODE39
BARCODE_ITF     = GS + '\x6b\x05'  # Barcode type ITF
BARCODE_NW7     = GS + '\x6b\x06'  # Barcode type NW7
# Image format
S_RASTER_N      = GS + '\x76\x30\x00'  # Set raster image normal size
S_RASTER_2W     = GS + '\x76\x30\x01'  # Set raster image double width
S_RASTER_2H     = GS + '\x76\x30\x02'  # Set raster image double height
S_RASTER_Q      = GS + '\x76\x30\x03'  # Set raster image quadruple
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
