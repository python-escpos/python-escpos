#!/usr/bin/python
""" Main class

This module contains the abstract base class :py:class:`Escpos`.

:author: `Manuel F Martinez <manpaz@bashlinux.com>`_ and others
:organization: Bashlinux and `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012 Bashlinux
:license: GNU GPL v3
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six

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
        :type msg: bytes
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
                return image_border // 2, image_border // 2
            else:
                return image_border // 2, (image_border // 2) + 1

    def _print_image(self, line, size):
        """ Print formatted image

        :param line:
        :param size:
        """
        i = 0
        cont = 0
        pbuffer = b''

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

        .. todo:: Seems to be broken. Write test that simply executes function with a dummy printer in order to
                  check for bugs like these in the future.

        :param path_img: complete filename and path to image of type `jpg`, `gif`, `png` or `bmp`
        """
        if not isinstance(path_img, Image.Image):
            im_open = Image.open(path_img)
        else:
            im_open = path_img

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
        """ Resizes and prints an arbitrarily sized image

        .. todo:: Seems to be broken. Write test that simply executes function with a dummy printer in order to
                  check for bugs like these in the future.
        """
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
        """ Direct printing function for pictures

        This function is rather fragile and will fail when the Image object is not suited.

        :param image: PIL image object, containing a 1-bit picture
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

    def barcode(self, code, bc, height=64, width=3, pos="BELOW", font="A", align_ct=True, function_type="A"):
        """ Print Barcode

        This method allows to print barcodes. The rendering of the barcode is done by the printer and therefore has to
        be supported by the unit. Currently you have to check manually whether your barcode text is correct. Uncorrect
        barcodes may lead to unexpected printer behaviour. There are two forms of the barcode function. Type A is
        default but has fewer barcodes, while type B has some more to choose from.

        .. todo:: Add a method to check barcode codes. Alternatively or as an addition write explanations about each
                  barcode-type. Research whether the check digits can be computed autmatically.

        Use the parameters `height` and `width` for adjusting of the barcode size. Please take notice that the barcode
        will not be printed if it is outside of the printable area. (Which should be impossible with this method, so
        this information is probably more useful for debugging purposes.)

        .. todo:: On TM-T88II width from 1 to 6 is accepted. Try to acquire command reference and correct the code.
        .. todo:: Supplying pos does not have an effect for every barcode type. Check and document for which types this
                  is true.

        If you do not want to center the barcode you can call the method with `align_ct=False`, which will disable
        automatic centering. Please note that when you use center alignment, then the alignment of text will be changed
        automatically to centered. You have to manually restore the alignment if necessary.

        .. todo:: If further barcode-types are needed they could be rendered transparently as an image. (This could also
                  be of help if the printer does not support types that others do.)
        
        :param code: alphanumeric data to be printed as bar code
        :param bc: barcode format, possible values are for type A are:

            * UPC-A
            * UPC-E
            * EAN13
            * EAN8
            * CODE39
            * ITF
            * NW7

            Possible values for type B:

            * All types from function type A
            * CODE93
            * CODE128
            * GS1-128
            * GS1 DataBar Omnidirectional
            * GS1 DataBar Truncated
            * GS1 DataBar Limited
            * GS1 DataBar Expanded

            If none is specified, the method raises :py:exc:`~escpos.exceptions.BarcodeTypeError`.
        :param height: barcode height, has to be between 1 and 255
            *default*: 64
        :type height: int
        :param width: barcode width, has to be between 2 and 6
            *default*: 3
        :type width: int
        :param pos: where to place the text relative to the barcode, *default*: BELOW

            * ABOVE
            * BELOW
            * BOTH
            * OFF

        :param font: select font (see ESC/POS-documentation, the device often has two fonts), *default*: A

            * A
            * B

        :param align_ct: If this parameter is True the barcode will be centered. Otherwise no alignment command will be
                         issued.
        :type align_ct: bool

        :param function_type: Choose between ESCPOS function type A or B, depending on printer support and desired
            barcode.
            *default*: A

        :raises: :py:exc:`~escpos.exceptions.BarcodeSizeError`,
                 :py:exc:`~escpos.exceptions.BarcodeTypeError`,
                 :py:exc:`~escpos.exceptions.BarcodeCodeError`
        """
        # Align Bar Code()
        if align_ct:
            self._raw(TXT_ALIGN_CT)
        # Height
        if 1 <= height <= 255:
            self._raw(BARCODE_HEIGHT + six.int2byte(height))
        else:
            raise BarcodeSizeError("height = {height}".format(height=height))
        # Width
        if 2 <= width <= 6:
            self._raw(BARCODE_WIDTH + six.int2byte(width))
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

        bc_types = BARCODE_TYPES[function_type.upper()]
        if bc.upper() not in bc_types.keys():
            # TODO: Raise a better error, or fix the message of this error type
            raise BarcodeTypeError("Barcode type {bc} not valid for barcode function type {function_type}".format(
                bc=bc,
                function_type=function_type,
            ))

        self._raw(bc_types[bc.upper()])

        if function_type.upper() == "B":
            self._raw(chr(len(code)))

        # Print Code
        if code:
            self._raw(code.encode())
        else:
            raise BarcodeCodeError()

        if function_type.upper() == "A":
            self._raw("\x00")

    def text(self, txt):
        """ Print alpha-numeric text

        The text has to be encoded in the currently selected codepage.

        .. todo:: rework this in order to proberly handle encoding

        :param txt: text to be printed
        :raises: :py:exc:`~escpos.exceptions.TextError`
        """
        if txt:
            self._raw(txt.encode())
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

    def set(self, align='left', font='a', text_type='normal', width=1, height=1, density=9, invert=False, smooth=False, flip=False):
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
            * U2 for underlined, version 2
            * BU for bold and underlined
            * BU2 for bold and underlined, version 2
            * NORMAL for normal text

            *default*: NORMAL
        :param width: text width multiplier, decimal range 1-8,  *default*: 1
        :param height: text height multiplier, decimal range 1-8, *default*: 1
        :param density: print density, value from 0-8, if something else is supplied the density remains unchanged
        :param invert: True enables white on black printing, *default*: False
        :param smooth: True enables text smoothing. Effective on 4x4 size text and larger, *default*: False
        :param flip: True enables upside-down printing, *default*: False
        :type invert: bool
        """
        # Width
        if height == 2 and width == 2:
            self._raw(TXT_NORMAL)
            self._raw(TXT_4SQUARE)
        elif height == 2 and width == 1:
            self._raw(TXT_NORMAL)
            self._raw(TXT_2HEIGHT)
        elif width == 2 and height == 1:
            self._raw(TXT_NORMAL)
            self._raw(TXT_2WIDTH)
        elif width == 1 and height == 1:
            self._raw(TXT_NORMAL)
        elif 1 <= width <= 8 and 1 <= height <= 8 and isinstance(width, int) and isinstance(height, int):
            self._raw(TXT_SIZE + six.int2byte(TXT_WIDTH[width] + TXT_HEIGHT[height]))
        else:
            raise SetVariableError()
        # Upside down
        if flip == True:
            self._raw(TXT_FLIP_ON)
        else:
            self._raw(TXT_FLIP_OFF)
        # Smoothing
        if smooth == True:
            self._raw(TXT_SMOOTH_ON)
        else:
            self._raw(TXT_SMOOTH_OFF)
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
        # Invert Printing
        if invert:
            self._raw(TXT_INVERT_ON)
        else:
            self._raw(TXT_INVERT_OFF)

    def cut(self, mode=''):
        """ Cut paper.

        Without any arguments the paper will be cut completely. With 'mode=PART' a partial cut will
        be attempted. Note however, that not all models can do a partial cut. See the documentation of
        your printer for details.
        .. todo:: Check this function on TM-T88II.

        :param mode: set to 'PART' for a partial cut
        """
        # Fix the size between last line and cut
        # TODO: handle this with a line feed
        self._raw(b"\n\n\n\n\n\n")
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
            self._raw(CTL_SET_HT + six.int2byte(pos))
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
