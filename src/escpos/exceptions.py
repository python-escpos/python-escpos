#  -*- coding: utf-8 -*-
""" ESC/POS Exceptions classes

Result/Exit codes:

    - `0`  = success
    - `10` = No Barcode type defined :py:exc:`~escpos.exceptions.BarcodeTypeError`
    - `20` = Barcode size values are out of range :py:exc:`~escpos.exceptions.BarcodeSizeError`
    - `30` = Barcode text not supplied :py:exc:`~escpos.exceptions.BarcodeCodeError`
    - `40` = Image height is too large :py:exc:`~escpos.exceptions.ImageSizeError`
    - `41` = Image width is too large :py:exc:`~escpos.exceptions.ImageWidthError`
    - `50` = No string supplied to be printed :py:exc:`~escpos.exceptions.TextError`
    - `60` = Invalid pin to send Cash Drawer pulse :py:exc:`~escpos.exceptions.CashDrawerError`
    - `70` = Invalid number of tab positions :py:exc:`~escpos.exceptions.TabPosError`
    - `80` = Invalid char code :py:exc:`~escpos.exceptions.CharCodeError`
    - `90` = USB device not found :py:exc:`~escpos.exceptions.USBNotFoundError`
    - `100` = Set variable out of range :py:exc:`~escpos.exceptions.SetVariableError`
    - `200` = Configuration not found :py:exc:`~escpos.exceptions.ConfigNotFoundError`
    - `210` = Configuration syntax error :py:exc:`~escpos.exceptions.ConfigSyntaxError`
    - `220` = Configuration section not found :py:exc:`~escpos.exceptions.ConfigSectionMissingError`

:author: `Manuel F Martinez <manpaz@bashlinux.com>`_ and others
:organization: Bashlinux and `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2017 Bashlinux and python-escpos
:license: MIT
"""


class Error(Exception):
    """Base class for ESC/POS errors"""

    def __init__(self, msg, status=None):
        Exception.__init__(self)
        self.msg = msg
        self.resultcode = 1
        if status is not None:
            self.resultcode = status

    def __str__(self):
        return self.msg


class BarcodeTypeError(Error):
    """No Barcode type defined.

    This exception indicates that no known barcode-type has been entered. The barcode-type has to be
    one of those specified in :py:meth:`escpos.escpos.Escpos.barcode`.
    The returned error code is `10`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 10

    def __str__(self):
        return "No Barcode type is defined ({msg})".format(msg=self.msg)


class BarcodeSizeError(Error):
    """Barcode size is out of range.

    This exception indicates that the values for the barcode size are out of range.
    The size of the barcode has to be in the range that is specified in :py:meth:`escpos.escpos.Escpos.barcode`.
    The resulting returncode is `20`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 20

    def __str__(self):
        return "Barcode size is out of range ({msg})".format(msg=self.msg)


class BarcodeCodeError(Error):
    """No Barcode code was supplied, or it is incorrect.

    No data for the barcode has been supplied in :py:meth:`escpos.escpos.Escpos.barcode` or the the `check` parameter
    was True and the check failed.
    The returncode for this exception is `30`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 30

    def __str__(self):
        return "No Barcode code was supplied ({msg})".format(msg=self.msg)


class ImageSizeError(Error):
    """Image height is longer than 255px and can't be printed.

    The returncode for this exception is `40`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 40

    def __str__(self):
        return "Image height is longer than 255px and can't be printed ({msg})".format(
            msg=self.msg
        )


class ImageWidthError(Error):
    """Image width is too large.

    The return code for this exception is `41`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 41

    def __str__(self):
        return "Image width is too large ({msg})".format(msg=self.msg)


class TextError(Error):
    """Text string must be supplied to the `text()` method.

    This exception is raised when an empty string is passed to :py:meth:`escpos.escpos.Escpos.text`.
    The returncode for this exception is `50`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 50

    def __str__(self):
        return "Text string must be supplied to the text() method ({msg})".format(
            msg=self.msg
        )


class CashDrawerError(Error):
    """Valid pin must be set in order to send pulse.

    A valid pin number has to be passed onto the method :py:meth:`escpos.escpos.Escpos.cashdraw`.
    The returncode for this exception is `60`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 60

    def __str__(self):
        return "Valid pin must be set to send pulse ({msg})".format(msg=self.msg)


class TabPosError(Error):
    """Valid tab positions must be set by using from 1 to 32 tabs, and between 1 and 255 tab size values.
    Both values multiplied must not exceed 255, since it is the maximum tab value.

    This exception is raised by :py:meth:`escpos.escpos.Escpos.control`.
    The returncode for this exception is `70`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 70

    def __str__(self):
        return "Valid tab positions must be in the range 0 to 16 ({msg})".format(
            msg=self.msg
        )


class CharCodeError(Error):
    """Valid char code must be set.

    The supplied charcode-name in :py:meth:`escpos.escpos.Escpos.charcode` is unknown.
    Ths returncode for this exception is `80`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 80

    def __str__(self):
        return "Valid char code must be set ({msg})".format(msg=self.msg)


class USBNotFoundError(Error):
    """Device wasn't found (probably not plugged in)

    The USB device seems to be not plugged in.
    Ths returncode for this exception is `90`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 90

    def __str__(self):
        return "USB device not found ({msg})".format(msg=self.msg)


class SetVariableError(Error):
    """A set method variable was out of range

    Check set variables against minimum and maximum values
    Ths returncode for this exception is `100`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 100

    def __str__(self):
        return "Set variable out of range ({msg})".format(msg=self.msg)


# Configuration errors


class ConfigNotFoundError(Error):
    """The configuration file was not found

    The default or passed configuration file could not be read
    Ths returncode for this exception is `200`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 200

    def __str__(self):
        return "Configuration not found ({msg})".format(msg=self.msg)


class ConfigSyntaxError(Error):
    """The configuration file is invalid

    The syntax is incorrect
    Ths returncode for this exception is `210`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 210

    def __str__(self):
        return "Configuration syntax is invalid ({msg})".format(msg=self.msg)


class ConfigSectionMissingError(Error):
    """The configuration file is missing a section

    The part of the config asked for doesn't exist in the loaded configuration
    Ths returncode for this exception is `220`.
    """

    def __init__(self, msg=""):
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 220

    def __str__(self):
        return "Configuration section is missing ({msg})".format(msg=self.msg)
