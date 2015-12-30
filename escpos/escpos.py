#!/usr/bin/python
"""
@author: Manuel F Martinez <manpaz@bashlinux.com>
@organization: Bashlinux
@copyright: Copyright (c) 2012 Bashlinux
@license: GNU GPL v3
"""

from PIL import Image, ImageOps

import struct
import qrcode
import time
import textwrap
import binascii
import operator

from .constants import *
from .exceptions import *

from abc import ABCMeta, abstractmethod  # abstract base class support

class Escpos(object):
    """ ESC/POS Printer object """
    __metaclass__ = ABCMeta
    device = None


    def __init__(self, columns=32):
        """ Initialize ESCPOS Printer

        :param columns: Text columns used by the printer. Defaults to 32."""
        self.columns = columns

    @abstractmethod
    def _raw(self, msg):
        """ Sends raw data to the printer

        This function has to be individually implemented by the implementations.
        :param msg: message string to be sent to the printer
        """
        pass

    @staticmethod
    def _check_image_size(size):
        """ Check and fix the size of the image to 32 bits

        :param size: size of the image
        :returns: tuple of image borders
        :rtype: (int, int)
        """
        if size % 32 == 0:
            return 0, 0
        else:
            image_border = 32 - (size % 32)
            if (image_border % 2) == 0:
                return (round(image_border / 2), round(image_border / 2))
            else:
                return (round(image_border / 2), round((image_border / 2) + 1))

    def _print_image(self, imagedata, n_rows, col_bytes):
        """ Print formatted image


        :param line:
        :param size:
        """
        self._raw(S_RASTER_N)
        pbuffer = struct.pack('<HH', col_bytes, n_rows)
        self._raw(pbuffer)
        self._raw(imagedata)
        pbuffer = ""

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
        im_left = ""
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

    def direct_image(self, image):
        """ Send image to printer"""
        mask = 0x80
        i = 0
        temp = 0

        (width, height) = image.size
        self._raw(S_RASTER_N)
        headerX = int(width / 8)
        headerY = height
        buf = "%02X" % (headerX & 0xff)
        buf += "%02X" % ((headerX >> 8) & 0xff)
        buf += "%02X" % (headerY & 0xff)
        buf += "%02X" % ((headerY >> 8) & 0xff)
        #self._raw(binascii.unhexlify(buf))
        for y in range(height):
            for x in range(width):
                value = image.getpixel((x,y))
                value = (value << 8) | value;
                if value == 0:
                    temp |= mask

                mask = mask >> 1

                i += 1
                if i == 8:
                    buf +=   ("%02X" % temp)
                    mask = 0x80
                    i = 0
                    temp = 0
        self._raw(binascii.unhexlify(bytes(buf, "ascii")))
        self._raw('\n')

    def qr(self, text, error_correction=qrcode.constants.ERROR_CORRECT_M):
        """ Print QR Code for the provided string

        :param text: text to generate a QR-Code from
        """
        qr_code = qrcode.QRCode(version=4, box_size=4, border=1, error_correction=error_correction)
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

    def charcode(self, code):
        """ Set Character Code Table

        Sends the control sequence from constants.py to the printer with :py:meth:`escpos.printer._raw()`.

        :param code: Name of CharCode
        :raises: CharCodeError
        """
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
        # elif code.upper() == "LATVIAN":  # this is not listed in the constants
        #    self._raw(CHARCODE_PC755)
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
        """ Print Barcode

        :param code: data for barcode
        :param bc: barcode format, see constants.py
        :param width: barcode width, has to be between 1 and 255
        :param height: barcode height, has to be between 2 and 6
        :param pos: position of text in barcode, default when nothing supplied is below
        :param font: select font, default is font A
        :raises: BarcodeSizeError, BarcodeTypeError, BarcodeCodeError
        """
        # Align Bar Code()
        self._raw(TXT_ALIGN_CT)
        # Height
        if height >= 2 or height <= 6:
            self._raw(BARCODE_HEIGHT)
        else:
            raise BarcodeSizeError()
        # Width
        if width >= 1 or width <= 255:
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
        elif bc.upper() in ("NW7", "CODABAR"):
            self._raw(BARCODE_NW7)
        else:
            raise BarcodeTypeError()
        # Print Code
        if code:
            self._raw(code)
        else:
            raise BarcodeCodeError()

    def text(self, txt):
        """ Print alpha-numeric text

        The text has to be encoded in the currently selected codepage.
        :param txt: text to be printed
        :raises: TextError
        """
        if txt:
            self._raw(txt)
        else:
            raise TextError()

    def block_text(self, txt, columns=None):
        '''Text is printed wrapped to specified columns'''
        colCount = self.columns if columns == None else columns
        self.text(textwrap.fill(txt, colCount))

    def set(self, align='left', font='a', text_type='normal', width=1, height=1, density=9):
        """ Set text properties by sending them to the printer

        :param align: alignment of text
        :param font: font A or B
        :param text_type: add bold or underlined
        :param width: text width, normal or double width
        :param height: text height, normal or double height
        :param density: print density
        """
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
        else:  # DEFAULT SIZE: NORMAL
            self._raw(TXT_NORMAL)
        # Type
        if text_type.upper() == "B":
            self._raw(TXT_BOLD_ON)
            self._raw(TXT_UNDERL_OFF)
        elif text_type.upper() == "U":
            self._raw(TXT_BOLD_OFF)
            self._raw(TXT_UNDERL_ON)
        elif text_type.upper() == "U2":
            self._raw(TXT_BOLD_OFF)
            self._raw(TXT_UNDERL2_ON)
        elif text_type.upper() == "BU":
            self._raw(TXT_BOLD_ON)
            self._raw(TXT_UNDERL_ON)
        elif text_type.upper() == "BU2":
            self._raw(TXT_BOLD_ON)
            self._raw(TXT_UNDERL2_ON)
        elif text_type.upper == "NORMAL":
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
        else:  # DEFAULT: DOES NOTHING
            pass

    def cut(self, mode=''):
        """ Cut paper

        :param mode: set to 'PART' for a partial cut
        """
        # Fix the size between last line and cut
        # TODO: handle this with a line feed
        self._raw("\n\n\n\n\n\n")
        if mode.upper() == "PART":
            self._raw(PAPER_PART_CUT)
        else: # DEFAULT MODE: FULL CUT
            self._raw(PAPER_FULL_CUT)

    def cashdraw(self, pin):
        """ Send pulse to kick the cash drawer

        Kick cash drawer on pin 2 or pin 5.
        :param pin: pin number
        :raises: CashDrawerError
        """
        if pin == 2:
            self._raw(CD_KICK_2)
        elif pin == 5:
            self._raw(CD_KICK_5)
        else:
            raise CashDrawerError()

    def hw(self, hw):
        """ Hardware operations

        :param hw: hardware action
        """
        if hw.upper() == "INIT":
            self._raw(HW_INIT)
        elif hw.upper() == "SELECT":
            self._raw(HW_SELECT)
        elif hw.upper() == "RESET":
            self._raw(HW_RESET)
        else: # DEFAULT: DOES NOTHING
            pass

    def control(self, ctl, pos=4):
        """ Feed control sequences

        :raises: TabPosError
        """
        # Set tab positions
        if pos < 1 or pos > 16:
            raise TabPosError()
        else:
            self._raw("".join([CTL_SET_HT, hex(pos)]))
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
