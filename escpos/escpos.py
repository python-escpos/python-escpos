#!/usr/bin/python
"""
@author: Manuel F Martinez <manpaz@bashlinux.com>
@organization: Bashlinux
@copyright: Copyright (c) 2012 Bashlinux
@license: GNU GPL v3
"""

try:
    import Image
except ImportError:
    from PIL import Image

import qrcode
import time

from constants import *
from exceptions import *

class Escpos:
    """ ESC/POS Printer object """
    device    = None


    def _check_image_size(self, size):
        """ Check and fix the size of the image to 32 bits """
        if size % 32 == 0:
            return (0, 0)
        else:
            image_border = 32 - (size % 32)
            if (image_border % 2) == 0:
                return (image_border / 2, image_border / 2)
            else:
                return (image_border / 2, (image_border / 2) + 1)


    def _print_image(self, line, size):
        """ Print formatted image """
        i = 0
        cont = 0
        buffer = ""
       
        self._raw(S_RASTER_N)
        buffer = "%02X%02X%02X%02X" % (((size[0]/size[1])/8), 0, size[1]&0xff, size[1]>>8)
        self._raw(buffer.decode('hex'))
        buffer = ""

        while i < len(line):
            hex_string = int(line[i:i+8],2)
            buffer += "%02X" % hex_string
            i += 8
            cont += 1
            if cont % 4 == 0:
                self._raw(buffer.decode("hex"))
                buffer = ""
                cont = 0


    def _convert_image(self, im):
        """ Parse image and prepare it to a printable format """
        pixels   = []
        pix_line = ""
        im_left  = ""
        im_right = ""
        switch   = 0
        img_size = [ 0, 0 ]


        if im.size[0] > 512:
            print  ("WARNING: Image is wider than 512 and could be truncated at print time ")
        if im.size[1] > 0xffff:
            raise ImageSizeError()

        im_border = self._check_image_size(im.size[0])
        for i in range(im_border[0]):
            im_left += "0"
        for i in range(im_border[1]):
            im_right += "0"

        for y in range(im.size[1]):
            img_size[1] += 1
            pix_line += im_left
            img_size[0] += im_border[0]
            for x in range(im.size[0]):
                img_size[0] += 1
                RGB = im.getpixel((x, y))
                im_color = (RGB[0] + RGB[1] + RGB[2])
                im_pattern = "1X0"
                pattern_len = len(im_pattern)
                switch = (switch - 1 ) * (-1)
                for x in range(pattern_len):
                    if im_color <= (255 * 3 / pattern_len * (x+1)):
                        if im_pattern[x] == "X":
                            pix_line += "%d" % switch
                        else:
                            pix_line += im_pattern[x]
                        break
                    elif im_color > (255 * 3 / pattern_len * pattern_len) and im_color <= (255 * 3):
                        pix_line += im_pattern[-1]
                        break 
            pix_line += im_right
            img_size[0] += im_border[1]

        self._print_image(pix_line, img_size)


    def image(self,path_img):
        """ Open image file """
        im_open = Image.open(path_img)

	# Remove the alpha channel on transparent images
	if im_open.mode == 'RGBA':
		im_open.load()
		im = Image.new("RGB", im_open.size, (255, 255, 255))
		im.paste(im_open, mask=im_open.split()[3])
	else:
	        im = im_open.convert("RGB")

        # Convert the RGB image in printable image
        self._convert_image(im)


    def qr(self,text):
        """ Print QR Code for the provided string """
        qr_code = qrcode.QRCode(version=4, box_size=4, border=1)
        qr_code.add_data(text)
        qr_code.make(fit=True)
        qr_img = qr_code.make_image()
        im = qr_img._img.convert("RGB")

        # Convert the RGB image in printable image
        self._convert_image(im)


    def charcode(self,code):
        """ Set Character Code Table """
        if code.upper() == "USA":
            self._raw(CHARCODE_PC437)
        elif code.upper() == "JIS":
            self._raw(CHARCODE_JIS)
        elif code.upper() == "MULTILINGUAL":
            self._raw(CHARCODE_PC850)
        elif code.upper() == "PORTUGUESE":
            self._raw(CHARCODE_PC860)
        elif code.upper() == "CA_FRENCH":
            self._raw(CHARCODE_PC863)
        elif code.upper() == "NORDIC":
            self._raw(CHARCODE_PC865)
        elif code.upper() == "WEST_EUROPE":
            self._raw(CHARCODE_WEU)
        elif code.upper() == "GREEK":
            self._raw(CHARCODE_GREEK)
        elif code.upper() == "HEBREW":
            self._raw(CHARCODE_HEBREW)
        elif code.upper() == "LATVIAN":
            self._raw(CHARCODE_PC755)
        elif code.upper() == "WPC1252":
            self._raw(CHARCODE_PC1252)
        elif code.upper() == "CIRILLIC2":
            self._raw(CHARCODE_PC866)
        elif code.upper() == "LATIN2":
            self._raw(CHARCODE_PC852)
        elif code.upper() == "EURO":
            self._raw(CHARCODE_PC858)
        elif code.upper() == "THAI42":
            self._raw(CHARCODE_THAI42)
        elif code.upper() == "THAI11":
            self._raw(CHARCODE_THAI11)
        elif code.upper() == "THAI13":
            self._raw(CHARCODE_THAI13)
        elif code.upper() == "THAI14":
            self._raw(CHARCODE_THAI14)
        elif code.upper() == "THAI16":
            self._raw(CHARCODE_THAI16)
        elif code.upper() == "THAI17":
            self._raw(CHARCODE_THAI17)
        elif code.upper() == "THAI18":
            self._raw(CHARCODE_THAI18)
        else:
            raise CharCodeError()

    def barcode(self, code, bc, width, height, pos, font):
        """ Print Barcode """
        # Align Bar Code()
        self._raw(TXT_ALIGN_CT)
        # Height
        if height >=2 or height <=6:
            self._raw(BARCODE_HEIGHT)
        else:
            raise BarcodeSizeError()
        # Width
        if width >= 1 or width <=255:
            self._raw(BARCODE_WIDTH)
        else:
            raise BarcodeSizeError()
        # Font
        if font.upper() == "B":
            self._raw(BARCODE_FONT_B)
        else: # DEFAULT FONT: A
            self._raw(BARCODE_FONT_A)
        # Position
        if pos.upper() == "OFF":
            self._raw(BARCODE_TXT_OFF)
        elif pos.upper() == "BOTH":
            self._raw(BARCODE_TXT_BTH)
        elif pos.upper() == "ABOVE":
            self._raw(BARCODE_TXT_ABV)
        else:  # DEFAULT POSITION: BELOW 
            self._raw(BARCODE_TXT_BLW)
        # Type 
        if bc.upper() == "UPC-A":
            self._raw(BARCODE_UPC_A)
        elif bc.upper() == "UPC-E":
            self._raw(BARCODE_UPC_E)
        elif bc.upper() == "EAN13":
            self._raw(BARCODE_EAN13)
        elif bc.upper() == "EAN8":
            self._raw(BARCODE_EAN8)
        elif bc.upper() == "CODE39":
            self._raw(BARCODE_CODE39)
        elif bc.upper() == "ITF":
            self._raw(BARCODE_ITF)
        elif bc.upper() == "NW7":
            self._raw(BARCODE_NW7)
        else:
            raise BarcodeTypeError()
        # Print Code
        if code:
            self._raw(code)
        else:
            raise exception.BarcodeCodeError()

        
    def text(self, txt):
        """ Print alpha-numeric text """
        if txt:
            self._raw(txt)
        else:
            raise TextError()


    def set(self, align='left', font='a', type='normal', width=1, height=1, density=9):
        """ Set text properties """
        # Width
        if height == 2 and width == 2:
            self._raw(TXT_NORMAL)
            self._raw(TXT_4SQUARE)
        elif height == 2 and width != 2:
            self._raw(TXT_NORMAL)
            self._raw(TXT_2HEIGHT)
        elif width == 2 and height != 2:
            self._raw(TXT_NORMAL)
            self._raw(TXT_2WIDTH)
        else: # DEFAULT SIZE: NORMAL
            self._raw(TXT_NORMAL)
        # Type
        if type.upper() == "B":
            self._raw(TXT_BOLD_ON)
            self._raw(TXT_UNDERL_OFF)
        elif type.upper() == "U":
            self._raw(TXT_BOLD_OFF)
            self._raw(TXT_UNDERL_ON)
        elif type.upper() == "U2":
            self._raw(TXT_BOLD_OFF)
            self._raw(TXT_UNDERL2_ON)
        elif type.upper() == "BU":
            self._raw(TXT_BOLD_ON)
            self._raw(TXT_UNDERL_ON)
        elif type.upper() == "BU2":
            self._raw(TXT_BOLD_ON)
            self._raw(TXT_UNDERL2_ON)
        elif type.upper == "NORMAL":
            self._raw(TXT_BOLD_OFF)
            self._raw(TXT_UNDERL_OFF)
        # Font
        if font.upper() == "B":
            self._raw(TXT_FONT_B)
        else:  # DEFAULT FONT: A
            self._raw(TXT_FONT_A)
        # Align
        if align.upper() == "CENTER":
            self._raw(TXT_ALIGN_CT)
        elif align.upper() == "RIGHT":
            self._raw(TXT_ALIGN_RT)
        elif align.upper() == "LEFT":
            self._raw(TXT_ALIGN_LT)
        # Density
        if density == 0:
            self._raw(PD_N50)
        elif density == 1:
            self._raw(PD_N37)
        elif density == 2:
            self._raw(PD_N25)
        elif density == 3:
            self._raw(PD_N12)
        elif density == 4:
            self._raw(PD_0)
        elif density == 5:
            self._raw(PD_P12)
        elif density == 6:
            self._raw(PD_P25)
        elif density == 7:
            self._raw(PD_P37)
        elif density == 8:
            self._raw(PD_P50)
        else:# DEFAULT: DOES NOTHING
            pass


    def cut(self, mode=''):
        """ Cut paper """
        # Fix the size between last line and cut
        # TODO: handle this with a line feed
        self._raw("\n\n\n\n\n\n")
        if mode.upper() == "PART":
            self._raw(PAPER_PART_CUT)
        else: # DEFAULT MODE: FULL CUT
            self._raw(PAPER_FULL_CUT)


    def cashdraw(self, pin):
        """ Send pulse to kick the cash drawer """
        if pin == 2:
            self._raw(CD_KICK_2)
        elif pin == 5:
            self._raw(CD_KICK_5)
        else:
            raise CashDrawerError()


    def hw(self, hw):
        """ Hardware operations """
        if hw.upper() == "INIT":
            self._raw(HW_INIT)
        elif hw.upper() == "SELECT":
            self._raw(HW_SELECT)
        elif hw.upper() == "RESET":
            self._raw(HW_RESET)
        else: # DEFAULT: DOES NOTHING
            pass


    def control(self, ctl, pos=4):
        """ Feed control sequences """
        # Set tab positions
        if pos < 1 or pos > 16:
            raise TabError()
        else:
            self._raw("".join([CTL_SET_HT,hex(pos)]))
        # Set position
        if ctl.upper() == "LF":
            self._raw(CTL_LF)
        elif ctl.upper() == "FF":
            self._raw(CTL_FF)
        elif ctl.upper() == "CR":
            self._raw(CTL_CR)
        elif ctl.upper() == "HT":
            self._raw(CTL_HT)
        elif ctl.upper() == "VT":
            self._raw(CTL_VT)
