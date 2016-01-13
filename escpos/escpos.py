#!/usr/bin/python
""" Main class

This module contains the abstract base class :py:class:`Escpos`.

:author: `Manuel F Martinez <manpaz@bashlinux.com>`_ and others
:organization: Bashlinux and `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012 Bashlinux
:license: GNU GPL v3
"""

try:
    import Image
except ImportError:
    from PIL import Image

import qrcode
import textwrap
import binascii
import operator

from .constants import *
from .exceptions import *

from abc import ABCMeta, abstractmethod  # abstract base class support


class Escpos(object):
    """ ESC/POS Printer object

    This class is the abstract base class for an esc/pos-printer. The printer implementations are children of this
    class.
    """
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
                return round(image_border / 2), round(image_border / 2)
            else:
                return round(image_border / 2), round((image_border / 2) + 1)

    def _print_image(self, line, size):
        """ Print formatted image

        :param line:
        :param size:
        """
        i = 0
        cont = 0
        pbuffer = ""

        self._raw(S_RASTER_N)
        pbuffer = "%02X%02X%02X%02X" % (((size[0]/size[1])/8), 0, size[1] & 0xff, size[1] >> 8)
        self._raw(binascii.unhexlify(pbuffer))
        pbuffer = ""

        while i < len(line):
            hex_string = int(line[i:i+8], 2)
            pbuffer += "%02X" % hex_string
            i += 8
            cont += 1
            if cont % 4 == 0:
                self._raw(binascii.unhexlify(pbuffer))
                pbuffer = ""
                cont = 0

    def _convert_image(self, im):
        """ Parse image and prepare it to a printable format

        :param im: image data
        :raises: :py:exc:`~escpos.exceptions.ImageSizeError`
        """
        pixels = []
        pix_line = ""
        im_left = ""
        im_right = ""
        switch = 0
        img_size = [0, 0]

        if im.size[0] > 512:
            print ("WARNING: Image is wider than 512 and could be truncated at print time ")
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
                switch = (switch - 1) * (-1)
                for x in range(pattern_len):
                    if im_color <= (255 * 3 / pattern_len * (x+1)):
                        if im_pattern[x] == "X":
                            pix_line += "%d" % switch
                        else:
                            pix_line += im_pattern[x]
                        break
                    elif (255 * 3 / pattern_len * pattern_len) < im_color <= (255 * 3):
                        pix_line += im_pattern[-1]
                        break
            pix_line += im_right
            img_size[0] += im_border[1]

        self._print_image(pix_line, img_size)

    def image(self, path_img):
        """ Open and print an image file

        Prints an image. The image is automatically adjusted in size in order to print it.

        :param path_img: complete filename and path to image of type `jpg`, `gif`, `png` or `bmp`
        """
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

    def fullimage(self, img, max_height=860, width=512, histeq=True, bandsize=255):
        """ Resizes and prints an arbitrarily sized image """
        if isinstance(img, (Image, Image.Image)):
            im = img.convert("RGB")
        else:
            im = Image.open(img).convert("RGB")

        if histeq:
            # Histogram equaliztion
            h = im.histogram()
            lut = []
            for b in range(0, len(h), 256):
                # step size
                step = reduce(operator.add, h[b:b+256]) / 255
                # create equalization lookup table
                n = 0
                for i in range(256):
                    lut.append(n / step)
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

    def direct_image(self, image):
        """ Send image to printer

        :param image:
        """
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
                value = image.getpixel((x, y))
                value |= (value << 8)
                if value == 0:
                    temp |= mask

                mask >>= 1

                i += 1
                if i == 8:
                    buf += ("%02X" % temp)
                    mask = 0x80
                    i = 0
                    temp = 0
        self._raw(binascii.unhexlify(bytes(buf, "ascii")))
        self._raw('\n')

    def qr(self, text):
        """ Print QR Code for the provided string

        Prints a QR-code. The size has been adjusted to version 4, so it is small enough to be
        printed but also big enough to be read by a smartphone.

        :param text: text to generate a QR-Code from
        """
        qr_code = qrcode.QRCode(version=4, box_size=4, border=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr_code.add_data(text)
        qr_code.make(fit=True)
        qr_img = qr_code.make_image()
        im = qr_img._img.convert("RGB")

        # Convert the RGB image in printable image
        self._convert_image(im)

    def charcode(self, code):
        """ Set Character Code Table

        Sends the control sequence from :py:mod:`escpos.constants` to the printer
        with :py:meth:`escpos.printer.'implementation'._raw()`.

        :param code: Name of CharCode
        :raises: :py:exc:`~escpos.exceptions.CharCodeError`
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

    def barcode(self, code, bc, height, width, pos, font):
        """ Print Barcode

        :param code: alphanumeric data to be printed as bar code
        :param bc: barcode format, possible values are:

            * UPC-A
            * UPC-E
            * EAN13
            * EAN8
            * CODE39
            * ITF
            * NW7

            If none is specified, the method raises :py:exc:`~escpos.exceptions.BarcodeTypeError`.
        :param height: barcode height, has to be between 2 and 6
            *default*: 3
        :param width: barcode width, has to be between 1 and 255
            *default*: 64
        :param pos: where to place the text relative to the barcode, *default*: below

            * ABOVE
            * BELOW
            * BOTH
            * OFF

        :param font: select font (see ESC/POS-documentation, the device often has two fonts), *default*: A

            * A
            * B

        :raises: :py:exc:`~escpos.exceptions.BarcodeSizeError`,
                 :py:exc:`~escpos.exceptions.BarcodeTypeError`,
                 :py:exc:`~escpos.exceptions.BarcodeCodeError`
        """
        # Align Bar Code()
        self._raw(TXT_ALIGN_CT)
        # Height
        if 1 <= height <= 255:
            self._raw(BARCODE_HEIGHT + chr(height))
        else:
            raise BarcodeSizeError("height = {height}".format(height=height))
        # Width
        if 2 <= width <= 6:
            self._raw(BARCODE_WIDTH + chr(width))
        else:
            raise BarcodeSizeError("width = {width}".format(width=width))
        # Font
        if font.upper() == "B":
            self._raw(BARCODE_FONT_B)
        else:  # DEFAULT FONT: A
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
            raise BarcodeCodeError()

    def text(self, txt):
        """ Print alpha-numeric text

        The text has to be encoded in the currently selected codepage.

        :param txt: text to be printed
        :raises: :py:exc:`~escpos.exceptions.TextError`
        """
        if txt:
            self._raw(txt)
        else:
            # TODO: why is it problematic to print an empty string?
            raise TextError()

    def block_text(self, txt, columns=None):
        """ Text is printed wrapped to specified columns

        :param txt: text to be printed
        :param columns: amount of columns
        :return: None
        """
        colCount = self.columns if columns is None else columns
        self.text(textwrap.fill(txt, colCount))

    def set(self, align='left', font='a', text_type='normal', width=1, height=1, density=9):
        """ Set text properties by sending them to the printer

        :param align: horizontal position for text, possible values are:

            * CENTER
            * LEFT
            * RIGHT

            *default*: LEFT
        :param font: font type, possible values are A or B, *default*: A
        :param text_type: text type, possible values are:

            * B for bold
            * U for underlined
            * B2 for bold, version 2
            * U2 for underlined, version 2
            * BU for bold and underlined
            * BU2 for bold and underlined, version 2
            * NORMAL for normal text

            *default*: NORMAL
        :param width: text width, normal (1) or double width (2), *default*: 1
        :param height: text height, normal (1) or double height (2), *default*: 1
        :param density: print density, value from 0-8, if something else is supplied the density remains unchanged
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
        """ Cut paper.

        Without any arguments the paper will be cut completely. With 'mode=PART' a partial cut will
        be attempted. Note however, that not all models can do a partial cut. See the documentation of
        your printer for details.

        :param mode: set to 'PART' for a partial cut
        """
        # Fix the size between last line and cut
        # TODO: handle this with a line feed
        self._raw("\n\n\n\n\n\n")
        if mode.upper() == "PART":
            self._raw(PAPER_PART_CUT)
        else:  # DEFAULT MODE: FULL CUT
            self._raw(PAPER_FULL_CUT)

    def cashdraw(self, pin):
        """ Send pulse to kick the cash drawer

        Kick cash drawer on pin 2 or pin 5 according to parameter.

        :param pin: pin number, 2 or 5
        :raises: :py:exc:`~escpos.exceptions.CashDrawerError`
        """
        if pin == 2:
            self._raw(CD_KICK_2)
        elif pin == 5:
            self._raw(CD_KICK_5)
        else:
            raise CashDrawerError()

    def hw(self, hw):
        """ Hardware operations

        :param hw: hardware action, may be:

            * INIT
            * SELECT
            * RESET
        """
        if hw.upper() == "INIT":
            self._raw(HW_INIT)
        elif hw.upper() == "SELECT":
            self._raw(HW_SELECT)
        elif hw.upper() == "RESET":
            self._raw(HW_RESET)
        else:  # DEFAULT: DOES NOTHING
            pass

    def control(self, ctl, pos=4):
        """ Feed control sequences

        :param ctl: string for the following control sequences:

            * LF *for Line Feed*
            * FF *for Form Feed*
            * CR *for Carriage Return*
            * HT *for Horizontal Tab*
            * VT *for Vertical Tab*

        :param pos: integer between 1 and 16, controls the horizontal tab position
        :raises: :py:exc:`~escpos.exceptions.TabPosError`
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
