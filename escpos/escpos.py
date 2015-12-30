#!/usr/bin/python
'''
@author: Manuel F Martinez <manpaz@bashlinux.com>
@organization: Bashlinux
@copyright: Copyright (c) 2012 Bashlinux
@license: GPL
'''
import struct
import os
import time
import qrcode
import operator
from PIL import Image, ImageOps

from escpos.utils import *
from escpos.constants import *
from escpos.exceptions import *

class Escpos(object):
    """ ESC/POS Printer object """
    device    = None

    def _check_image_size(self, size):
        """ Check and fix the size of the image to 32 bits """
        if size % 32 == 0:
            return (0, 0)
        else:
            image_border = 32 - (size % 32)
            if (image_border % 2) == 0:
                return (image_border // 2, image_border // 2)
            else:
                return (image_border // 2, image_border // 2 + 1)

    def _print_image(self, imagedata, n_rows, col_bytes):
        """ Print formatted image """
        i = 0
        cont = 0
        buffer = ""

        self._raw(S_RASTER_N)
        buffer = struct.pack('<HH', col_bytes, n_rows)
        self._raw(buffer)
        self._raw(imagedata)

    def fullimage(self, img, max_height=860, width=512, histeq=True, bandsize=255):
        """ Resizes and prints an arbitrarily sized image """
        if isinstance(img, Image.Image):
            im = img.convert("RGB")
        else:
            im = Image.open(img).convert("RGB")

        if histeq:
            # Histogram equaliztion
            h = im.histogram()
            lut = []
            for b in range(0, len(h), 256):
                # step size
                step = reduce(operator.add, h[b:b+256]) // 255
                # create equalization lookup table
                n = 0
                for i in range(256):
                    lut.append(n // step)
                    n = n + h[i+b]
            im = im.point(lut)

        if width:
            ratio = float(width) / im.size[0]
            newheight = int(ratio * im.size[1])

            # Resize the image
            im = im.resize((width, newheight), Image.ANTIALIAS)

        if max_height and im.size[1] > max_height:
            im = im.crop((0, 0, im.size[0], max_height))

        # Divide into bands
        current = 0
        while current < im.size[1]:
            self.image(im.crop((0, current, width or im.size[0],
                                min(im.size[1], current + bandsize))))
            current += bandsize

    def image(self, im):
        """ Parse image and prepare it to a printable format """
        pixels   = []
        pix_line = ""
        im_left  = ""
        im_right = ""
        switch   = 0
        img_size = [ 0, 0 ]

        if not isinstance(im, Image.Image):
            im = Image.open(im)

        im = im.convert("L")
        im = ImageOps.invert(im)
        im = im.convert("1")

        if im.size[0] > 640:
            print("WARNING: Image is wider than 640 and could be truncated at print time ")
        if im.size[1] > 640:
            raise ImageSizeError()
 
        orig_width, height = im.size
        width = ((orig_width + 31) // 32) * 32
        new_image = Image.new("1", (width, height))
        new_image.paste(im, (0, 0, orig_width, height))

        the_bytes = new_image.tobytes()
        self._print_image(the_bytes, n_rows=height, col_bytes=width//8)

    def qr(self, text):
        """ Print QR Code for the provided string """
        qr_code = qrcode.QRCode(version=4, box_size=4, border=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr_code.add_data(text)
        qr_code.make(fit=True)
        qr_img = qr_code.make_image()
        # Convert the RGB image in printable image
        im = qr_img._img.convert("1")
        width = im.size[0]
        height = im.size[1]
        while width * 2 <= 640:
             width *= 2
             height *= 2

        im = im.resize((width, height))
        self.image(im)
        self.text('\n')

    def barcode(self, code, bc, height, width, pos, font):
        """ Print Barcode """
        # Align Bar Code()
        self._raw(TXT_ALIGN_CT)
        # Height
        if 1 <= height <= 255:
            self._raw(BARCODE_HEIGHT + chr(height))
        else:
            raise BarcodeSizeError("height = %s" % height)
        # Width
        if 2 <= width <= 6:
            self._raw(BARCODE_WIDTH + chr(width))
        else:
            raise BarcodeSizeError("width = %s" % width)
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
        elif bc.upper() in ("NW7", "CODABAR"):
            self._raw(BARCODE_NW7)
        else:
            raise BarcodeTypeError(bc)
        # Print Code
        if code:
            self._raw(code)
        else:
            raise exception.BarcodeCodeError()

    def text(self, txt):
        """ Print alpha-numeric text """
        if txt:
            self._raw(txt.encode('cp936'))
        else:
            raise TextError()

    def set(self, align='left', font='a', type='normal', width=1, height=1):
        """ Set text properties """
        # Width
        if height != 2 and width != 2: # DEFAULT SIZE: NORMAL
            self._raw(TXT_NORMAL)

        if height == 2:
            self._raw(TXT_2HEIGHT)
        if width == 2:
            self._raw(TXT_2WIDTH)

        if height == 2 and width == 2:
            self._raw(TXT_4SQUARE)

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
            self._raw(TXT_ITALIC_OFF)
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

    def control(self, ctl):
        """ Feed control sequences """
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
