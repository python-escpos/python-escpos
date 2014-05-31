""" ESC/POS Commands (Constants) """

from escpos.utils import hex2bytes

# Feed control sequences
CTL_LF    = hex2bytes('0a')             # Print and line feed
CTL_FF    = hex2bytes('0c')             # Form feed
CTL_CR    = hex2bytes('0d')             # Carriage return
CTL_HT    = hex2bytes('09')             # Horizontal tab
CTL_VT    = hex2bytes('0b')             # Vertical tab
# Printer hardware
HW_INIT   = hex2bytes('1b40')         # Clear data in buffer and reset modes
HW_SELECT = hex2bytes('1b3d01')     # Printer select
HW_RESET  = hex2bytes('1b3f0a00') # Reset printer hardware
# Cash Drawer
CD_KICK_2 = hex2bytes('1b7000')     # Sends a pulse to pin 2 [] 
CD_KICK_5 = hex2bytes('1b7001')     # Sends a pulse to pin 5 [] 
# Paper
PAPER_FULL_CUT  = hex2bytes('1d5600') # Full cut paper
PAPER_PART_CUT  = hex2bytes('1d5601') # Partial cut paper
# Text format   
TXT_NORMAL      = hex2bytes('1b2100') # Normal text
TXT_2HEIGHT     = hex2bytes('1b2110') # Double height text
TXT_2WIDTH      = hex2bytes('1b2120') # Double width text
TXT_4SQUARE     = hex2bytes('1b2130') # Quad area text
TXT_UNDERL_OFF  = hex2bytes('1b2d00') # Underline font OFF
TXT_UNDERL_ON   = hex2bytes('1b2d01') # Underline font 1-dot ON
TXT_UNDERL2_ON  = hex2bytes('1b2d02') # Underline font 2-dot ON
TXT_BOLD_OFF    = hex2bytes('1b4500') # Bold font OFF
TXT_BOLD_ON     = hex2bytes('1b4501') # Bold font ON
TXT_FONT_A      = hex2bytes('1b4d00') # Font type A
TXT_FONT_B      = hex2bytes('1b4d01') # Font type B
TXT_ALIGN_LT    = hex2bytes('1b6100') # Left justification
TXT_ALIGN_CT    = hex2bytes('1b6101') # Centering
TXT_ALIGN_RT    = hex2bytes('1b6102') # Right justification
# Barcode format
BARCODE_TXT_OFF = hex2bytes('1d4800') # HRI barcode chars OFF
BARCODE_TXT_ABV = hex2bytes('1d4801') # HRI barcode chars above
BARCODE_TXT_BLW = hex2bytes('1d4802') # HRI barcode chars below
BARCODE_TXT_BTH = hex2bytes('1d4803') # HRI barcode chars both above and below
BARCODE_FONT_A  = hex2bytes('1d6600') # Font type A for HRI barcode chars
BARCODE_FONT_B  = hex2bytes('1d6601') # Font type B for HRI barcode chars
BARCODE_HEIGHT  = hex2bytes('1d6864') # Barcode Height [1-255]
BARCODE_WIDTH   = hex2bytes('1d7703') # Barcode Width  [2-6]
BARCODE_UPC_A   = hex2bytes('1d6b00') # Barcode type UPC-A
BARCODE_UPC_E   = hex2bytes('1d6b01') # Barcode type UPC-E
BARCODE_EAN13   = hex2bytes('1d6b02') # Barcode type EAN13
BARCODE_EAN8    = hex2bytes('1d6b03') # Barcode type EAN8
BARCODE_CODE39  = hex2bytes('1d6b04') # Barcode type CODE39
BARCODE_ITF     = hex2bytes('1d6b05') # Barcode type ITF
BARCODE_NW7     = hex2bytes('1d6b06') # Barcode type NW7
# Image format  
S_RASTER_N      = hex2bytes('1d763000') # Set raster image normal size
S_RASTER_2W     = hex2bytes('1d763001') # Set raster image double width
S_RASTER_2H     = hex2bytes('1d763002') # Set raster image double height
S_RASTER_Q      = hex2bytes('1d763003') # Set raster image quadruple
