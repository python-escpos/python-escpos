#!/usr/bin/python
#  -*- coding: utf-8 -*-
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

import qrcode
import textwrap

from .constants import *
from .exceptions import *

from abc import ABCMeta, abstractmethod  # abstract base class support
from escpos.image import EscposImage


@six.add_metaclass(ABCMeta)
class Escpos(object):
    """ ESC/POS Printer object

    This class is the abstract base class for an esc/pos-printer. The printer implementations are children of this
    class.
    """
    device = None
    codepage = None

    def __init__(self, columns=32):
        """ Initialize ESCPOS Printer

        :param columns: Text columns used by the printer. Defaults to 32."""
        self.columns = columns

    def __del__(self):
        """ call self.close upon deletion """
        self.close()

    @abstractmethod
    def _raw(self, msg):
        """ Sends raw data to the printer

        This function has to be individually implemented by the implementations.

        :param msg: message string to be sent to the printer
        :type msg: bytes
        """
        pass

    def image(self, img_source, high_density_vertical=True, high_density_horizontal=True, impl="bitImageRaster",
              fragment_height=1024):
        """ Print an image

        You can select whether the printer should print in high density or not. The default value is high density.
        When printing in low density, the image will be stretched.

        Esc/Pos supplies several commands for printing. This function supports three of them. Please try to vary the
        implementations if you have any problems. For example the printer `IT80-002` will have trouble aligning
        images that are not printed in Column-mode.

        The available printing implementations are:

            * `bitImageRaster`: prints with the `GS v 0`-command
            * `graphics`: prints with the `GS ( L`-command
            * `bitImageColumn`: prints with the `ESC *`-command

        :param img_source: PIL image or filename to load: `jpg`, `gif`, `png` or `bmp`
        :param high_density_vertical: print in high density in vertical direction *default:* True
        :param high_density_horizontal: print in high density in horizontal direction *default:* True
        :param impl: choose image printing mode between `bitImageRaster`, `graphics` or `bitImageColumn`
        :param fragment_height: Images larger than this will be split into multiple fragments *default:* 1024

        """       
        im = EscposImage(img_source)

        if im.height > fragment_height:
            fragments = im.split(fragment_height)
            for fragment in fragments:
                self.image(fragment,
                           high_density_vertical=high_density_vertical,
                           high_density_horizontal=high_density_horizontal,
                           impl=impl,
                           fragment_height=fragment_height)
            return
        
        if impl == "bitImageRaster":
            # GS v 0, raster format bit image
            density_byte = (0 if high_density_horizontal else 1) + (0 if high_density_vertical else 2)
            header = GS + b"v0" + six.int2byte(density_byte) + self._int_low_high(im.width_bytes, 2) + self._int_low_high(im.height, 2)
            self._raw(header + im.to_raster_format())
        
        if impl == "graphics":
            # GS ( L raster format graphics
            img_header = self._int_low_high(im.width, 2) + self._int_low_high(im.height, 2)
            tone = b'0'
            colors = b'1'
            ym = six.int2byte(1 if high_density_vertical else 2)
            xm = six.int2byte(1 if high_density_horizontal else 2)
            header = tone + xm + ym + colors + img_header
            raster_data = im.to_raster_format()
            self._image_send_graphics_data(b'0', b'p', header + raster_data)
            self._image_send_graphics_data(b'0', b'2', b'')
        
        if impl == "bitImageColumn":
            # ESC *, column format bit image
            density_byte = (1 if high_density_horizontal else 0) + (32 if high_density_vertical else 0)
            header = ESC + b"*" + six.int2byte(density_byte) + self._int_low_high(im.width, 2)
            outp = [ESC + b"3" + six.int2byte(16)]  # Adjust line-feed size
            for blob in im.to_column_format(high_density_vertical):
                outp.append(header + blob + b"\n")
            outp.append(ESC + b"2")  # Reset line-feed size
            self._raw(b''.join(outp))

    def _image_send_graphics_data(self, m, fn, data):
        """
        Wrapper for GS ( L, to calculate and send correct data length.
        
        :param m: Modifier//variant for function. Usually '0'
        :param fn: Function number to use, as byte
        :param data: Data to send
        """
        header = self._int_low_high(len(data) + 2, 2)
        self._raw(GS + b'(L' + header + m + fn + data)

    def qr(self, content, ec=QR_ECLEVEL_L, size=3, model=QR_MODEL_2, native=False):
        """ Print QR Code for the provided string

        :param content: The content of the code. Numeric data will be more efficiently compacted.
        :param ec: Error-correction level to use. One of QR_ECLEVEL_L (default), QR_ECLEVEL_M, QR_ECLEVEL_Q or
            QR_ECLEVEL_H.
            Higher error correction results in a less compact code.
        :param size: Pixel size to use. Must be 1-16 (default 3)
        :param model: QR code model to use. Must be one of QR_MODEL_1, QR_MODEL_2 (default) or QR_MICRO (not supported
            by all printers).
        :param native: True to render the code on the printer, False to render the code as an image and send it to the
            printer (Default)
        """
        # Basic validation
        if ec not in [QR_ECLEVEL_L, QR_ECLEVEL_M, QR_ECLEVEL_H, QR_ECLEVEL_Q]:
            raise ValueError("Invalid error correction level")
        if not 1 <= size <= 16:
            raise ValueError("Invalid block size (must be 1-16)")
        if model not in [QR_MODEL_1, QR_MODEL_2, QR_MICRO]:
            raise ValueError("Invalid QR model (must be one of QR_MODEL_1, QR_MODEL_2, QR_MICRO)")
        if content == "":
            # Handle edge case by printing nothing.
            return
        if not native:
            # Map ESC/POS error correction levels to python 'qrcode' library constant and render to an image
            if model != QR_MODEL_2:
                raise ValueError("Invalid QR model for qrlib rendering (must be QR_MODEL_2)")
            python_qr_ec = {
                QR_ECLEVEL_H: qrcode.constants.ERROR_CORRECT_H,
                QR_ECLEVEL_L: qrcode.constants.ERROR_CORRECT_L,
                QR_ECLEVEL_M: qrcode.constants.ERROR_CORRECT_M,
                QR_ECLEVEL_Q: qrcode.constants.ERROR_CORRECT_Q
            }
            qr_code = qrcode.QRCode(version=None, box_size=size, border=1, error_correction=python_qr_ec[ec])
            qr_code.add_data(content)
            qr_code.make(fit=True)
            qr_img = qr_code.make_image()
            im = qr_img._img.convert("RGB")
            # Convert the RGB image in printable image
            self.image(im)
            return
        # Native 2D code printing
        cn = b'1'  # Code type for QR code
        # Select model: 1, 2 or micro.
        self._send_2d_code_data(six.int2byte(65), cn, six.int2byte(48 + model) + six.int2byte(0))
        # Set dot size.
        self._send_2d_code_data(six.int2byte(67), cn, six.int2byte(size))
        # Set error correction level: L, M, Q, or H
        self._send_2d_code_data(six.int2byte(69), cn, six.int2byte(48 + ec))
        # Send content & print
        self._send_2d_code_data(six.int2byte(80), cn, content.encode('utf-8'), b'0')
        self._send_2d_code_data(six.int2byte(81), cn, b'', b'0')

    def _send_2d_code_data(self, fn, cn, data, m=b''):
        """ Wrapper for GS ( k, to calculate and send correct data length.

        :param fn: Function to use.
        :param cn: Output code type. Affects available data.
        :param data: Data to send.
        :param m: Modifier/variant for function. Often '0' where used.
        """
        if len(m) > 1 or len(cn) != 1 or len(fn) != 1:
            raise ValueError("cn and fn must be one byte each.")
        header = self._int_low_high(len(data) + len(m) + 2, 2)
        self._raw(GS + b'(k' + header + cn + fn + m + data)
    
    @staticmethod
    def _int_low_high(inp_number, out_bytes):
        """ Generate multiple bytes for a number: In lower and higher parts, or more parts as needed.
        
        :param inp_number: Input number
        :param out_bytes: The number of bytes to output (1 - 4).
        """
        max_input = (256 << (out_bytes * 8) - 1)
        if not 1 <= out_bytes <= 4:
            raise ValueError("Can only output 1-4 byes")
        if not 0 <= inp_number <= max_input:
            raise ValueError("Number too large. Can only output up to {0} in {1} byes".format(max_input, out_bytes))
        outp = b''
        for _ in range(0, out_bytes):
            outp += six.int2byte(inp_number % 256)
            inp_number //= 256
        return outp

    def charcode(self, code):
        """ Set Character Code Table

        Sends the control sequence from :py:mod:`escpos.constants` to the printer
        with :py:meth:`escpos.printer.'implementation'._raw()`.

        :param code: Name of CharCode
        :raises: :py:exc:`~escpos.exceptions.CharCodeError`
        """
        # TODO improve this (rather unhandy code)
        # TODO check the codepages
        if code.upper() == "USA":
            self._raw(CHARCODE_PC437)
            self.codepage = 'cp437'
        elif code.upper() == "JIS":
            self._raw(CHARCODE_JIS)
            self.codepage = 'cp932'
        elif code.upper() == "MULTILINGUAL":
            self._raw(CHARCODE_PC850)
            self.codepage = 'cp850'
        elif code.upper() == "PORTUGUESE":
            self._raw(CHARCODE_PC860)
            self.codepage = 'cp860'
        elif code.upper() == "CA_FRENCH":
            self._raw(CHARCODE_PC863)
            self.codepage = 'cp863'
        elif code.upper() == "NORDIC":
            self._raw(CHARCODE_PC865)
            self.codepage = 'cp865'
        elif code.upper() == "WEST_EUROPE":
            self._raw(CHARCODE_WEU)
            self.codepage = 'latin_1'
        elif code.upper() == "GREEK":
            self._raw(CHARCODE_GREEK)
            self.codepage = 'cp737'
        elif code.upper() == "HEBREW":
            self._raw(CHARCODE_HEBREW)
            self.codepage = 'cp862'
        # elif code.upper() == "LATVIAN":  # this is not listed in the constants
        #    self._raw(CHARCODE_PC755)
        #    self.codepage = 'cp'
        elif code.upper() == "WPC1252":
            self._raw(CHARCODE_PC1252)
            self.codepage = 'cp1252'
        elif code.upper() == "CIRILLIC2":
            self._raw(CHARCODE_PC866)
            self.codepage = 'cp866'
        elif code.upper() == "LATIN2":
            self._raw(CHARCODE_PC852)
            self.codepage = 'cp852'
        elif code.upper() == "EURO":
            self._raw(CHARCODE_PC858)
            self.codepage = 'cp858'
        elif code.upper() == "THAI42":
            self._raw(CHARCODE_THAI42)
            self.codepage = 'cp874'
        elif code.upper() == "THAI11":
            self._raw(CHARCODE_THAI11)
            self.codepage = 'cp874'
        elif code.upper() == "THAI13":
            self._raw(CHARCODE_THAI13)
            self.codepage = 'cp874'
        elif code.upper() == "THAI14":
            self._raw(CHARCODE_THAI14)
            self.codepage = 'cp874'
        elif code.upper() == "THAI16":
            self._raw(CHARCODE_THAI16)
            self.codepage = 'cp874'
        elif code.upper() == "THAI17":
            self._raw(CHARCODE_THAI17)
            self.codepage = 'cp874'
        elif code.upper() == "THAI18":
            self._raw(CHARCODE_THAI18)
            self.codepage = 'cp874'
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
            self._raw(six.int2byte(len(code)))

        # Print Code
        if code:
            self._raw(code.encode())
        else:
            raise BarcodeCodeError()

        if function_type.upper() == "A":
            self._raw(NUL)

    def text(self, txt):
        """ Print alpha-numeric text

        The text has to be encoded in the currently selected codepage.
        The input text has to be encoded in unicode.

        :param txt: text to be printed
        :raises: :py:exc:`~escpos.exceptions.TextError`
        """
        if txt:
            if self.codepage:
                self._raw(txt.encode(self.codepage))
            else:
                self._raw(txt.encode())
        else:
            # TODO: why is it problematic to print an empty string?
            raise TextError()

    def block_text(self, txt, columns=None):
        """ Text is printed wrapped to specified columns

        Text has to be encoded in unicode.

        :param txt: text to be printed
        :param columns: amount of columns
        :return: None
        """
        col_count = self.columns if columns is None else columns
        self.text(textwrap.fill(txt, col_count))

    def set(self, align='left', font='a', text_type='normal', width=1, height=1, density=9, invert=False, smooth=False,
            flip=False):
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
        if flip:
            self._raw(TXT_FLIP_ON)
        else:
            self._raw(TXT_FLIP_OFF)
        # Smoothing
        if smooth:
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
        elif text_type.upper() == "NORMAL":
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

    def line_spacing(self, spacing=None, divisor=180):
        """ Set line character spacing.

        If no spacing is given, we reset it to the default.

        There are different commands for setting the line spacing, using
        a different denominator:

        '+'' line_spacing/360 of an inch, 0 <= line_spacing <= 255
        '3' line_spacing/180 of an inch, 0 <= line_spacing <= 255
        'A' line_spacing/60 of an inch, 0 <= line_spacing <= 85

        Some printers may not support all of them. The most commonly
        available command (using a divisor of 180) is chosen.
        """
        if spacing is None:
            self._raw(LINESPACING_RESET)
            return

        if divisor not in LINESPACING_FUNCS:
            raise ValueError("divisor must be either 360, 180 or 60")
        if (divisor in [360, 180] \
                and (not(0 <= spacing <= 255))):
            raise ValueError("spacing must be a int between 0 and 255 when divisor is 360 or 180")
        if divisor == 60 and (not(0 <= spacing <= 85)):
            raise ValueError("spacing must be a int between 0 and 85 when divisor is 60")

        self._raw(LINESPACING_FUNCS[divisor] + six.int2byte(spacing))

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
        if not (1 <= pos <= 16):
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

    def panel_buttons(self, enable=True):
        """ Controls the panel buttons on the printer (e.g. FEED)

        When enable is set to False the panel buttons on the printer will be disabled. Calling the method with
        enable=True or without argument will enable the panel buttons.

        If panel buttons are enabled, the function of the panel button, such as feeding, will be executed upon pressing
        the button. If the panel buttons are disabled, pressing them will not have any effect.

        This command is effective until the printer is initialized, reset or power-cycled. The default is enabled panel
        buttons.

        Some panel buttons will always work, especially when printer is opened. See for more information the manual
        of your printer and the escpos-command-reference.

        :param enable: controls the panel buttons
        :rtype: None
        """
        if enable:
            self._raw(PANEL_BUTTON_ON)
        else:
            self._raw(PANEL_BUTTON_OFF)


class EscposIO(object):
    """ESC/POS Printer IO object

    Allows the class to be used together with the `with`-statement. You have to define a printer instance
    and assign it to the EsposIO-class.
    This example explains the usage:

    .. code-block:: Python

        with EscposIO(printer.Serial('/dev/ttyUSB0')) as p:
            p.set(font='a', height=2, align='center', text_type='bold')
            p.printer.set(align='left')
            p.printer.image('logo.gif')
            p.writelines('Big line\\n', font='b')
            p.writelines('Привет')
            p.writelines('BIG TEXT', width=2)

    After the `with`-statement the printer automatically cuts the paper if `autocut` is `True`.
    """

    def __init__(self, printer, autocut=True, autoclose=True, **kwargs):
        """
        :param printer: An EscPos-printer object
        :type printer: escpos.Escpos
        :param autocut: If True, paper is automatically cut after the `with`-statement *default*: True
        :param kwargs: These arguments will be passed to :py:meth:`escpos.Escpos.set()`
        """
        self.printer = printer
        self.params = kwargs
        self.autocut = autocut
        self.autoclose = autoclose

    def set(self, **kwargs):
        """ Set the printer-parameters

        Controls which parameters will be passed to :py:meth:`Escpos.set() <escpos.escpos.Escpos.set()>`.
        For more information on the parameters see the :py:meth:`set() <escpos.escpos.Escpos.set()>`-methods
        documentation. These parameters can also be passed with this class' constructor or the
        :py:meth:`~escpos.escpos.EscposIO.writelines()`-method.

        :param kwargs: keyword-parameters that will be passed to :py:meth:`Escpos.set() <escpos.escpos.Escpos.set()>`
        """
        self.params.update(kwargs)

    def writelines(self, text, **kwargs):
        params = dict(self.params)
        params.update(kwargs)

        if isinstance(text, six.text_type):
            lines = text.split('\n')
        elif isinstance(text, list) or isinstance(text, tuple):
            lines = text
        else:
            lines = ["{0}".format(text), ]

        # TODO check unicode handling
        # TODO flush? or on print? (this should prob rather be handled by the _raw-method)
        for line in lines:
            self.printer.set(**params)
            if isinstance(text, six.text_type):
                self.printer.text(u"{0}\n".format(line))
            else:
                self.printer.text("{0}\n".format(line))

    def close(self):
        """ called upon closing the `with`-statement
        """
        self.printer.close()

    def __enter__(self, **kwargs):
        return self

    def __exit__(self, type, value, traceback):
        """

        If :py:attr:`autocut <escpos.escpos.EscposIO.autocut>` is `True` (set by this class' constructor),
        then :py:meth:`printer.cut() <escpos.escpos.Escpos.cut()>` will be called here.
        """
        if not (type is not None and issubclass(type, Exception)):
            if self.autocut:
                self.printer.cut()

        if self.autoclose:
            self.close()
