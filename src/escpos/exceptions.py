#  -*- coding: utf-8 -*-
"""ESC/POS Exceptions classes.

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
    - `90` = Device not found :py:exc:`~escpos.exceptions.DeviceNotFoundError`
    - `91` = USB device not found :py:exc:`~escpos.exceptions.USBNotFoundError`
    - `100` = Set variable out of range :py:exc:`~escpos.exceptions.SetVariableError`
    - `200` = Configuration not found :py:exc:`~escpos.exceptions.ConfigNotFoundError`
    - `210` = Configuration syntax error :py:exc:`~escpos.exceptions.ConfigSyntaxError`
    - `220` = Configuration section not found :py:exc:`~escpos.exceptions.ConfigSectionMissingError`

:author: python-escpos developers
:organization: Bashlinux and `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2017 Bashlinux and python-escpos
:license: MIT
"""

from typing import Optional


class Error(Exception):
    """Base class for ESC/POS errors.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.Error
        :parts: 1

    """

    def __init__(self, msg: str, status: Optional[int] = None) -> None:
        """Initialize Error object."""
        Exception.__init__(self)
        self.msg = msg
        self.resultcode = 1
        if status is not None:
            self.resultcode = status

    def __str__(self) -> str:
        """Return string representation of Error."""
        return self.msg


class BarcodeTypeError(Error):
    """No Barcode type defined.

    This exception indicates that no known barcode-type has been entered. The barcode-type has to be
    one of those specified in :py:meth:`escpos.escpos.Escpos.barcode`.
    The returned error code is `10`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.BarcodeTypeError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize BarcodeTypeError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 10

    def __str__(self) -> str:
        """Return string representation of BarcodeTypeError."""
        return f"No Barcode type is defined ({self.msg})"


class BarcodeSizeError(Error):
    """Barcode size is out of range.

    This exception indicates that the values for the barcode size are out of range.
    The size of the barcode has to be in the range that is specified in :py:meth:`escpos.escpos.Escpos.barcode`.
    The resulting return code is `20`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.BarcodeSizeError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize BarcodeSizeError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 20

    def __str__(self) -> str:
        """Return string representation of BarcodeSizeError."""
        return f"Barcode size is out of range ({self.msg})"


class BarcodeCodeError(Error):
    """No Barcode code was supplied, or it is incorrect.

    No data for the barcode has been supplied in :py:meth:`escpos.escpos.Escpos.barcode` or the the `check` parameter
    was True and the check failed.
    The return code for this exception is `30`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.BarcodeCodeError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize BarcodeCodeError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 30

    def __str__(self) -> str:
        """Return string representation of BarcodeCodeError."""
        return f"No Barcode code was supplied ({self.msg})"


class ImageSizeError(Error):
    """Image height is longer than 255px and can't be printed.

    The return code for this exception is `40`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.ImageSizeError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize ImageSizeError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 40

    def __str__(self) -> str:
        """Return string representation of ImageSizeError."""
        return f"Image height is longer than 255px and can't be printed ({self.msg})"


class ImageWidthError(Error):
    """Image width is too large.

    The return code for this exception is `41`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.ImageWidthError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize ImageWidthError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 41

    def __str__(self) -> str:
        """Return string representation of ImageWidthError."""
        return f"Image width is too large ({self.msg})"


class TextError(Error):
    """Text string must be supplied to the `text()` method.

    This exception is raised when an empty string is passed to :py:meth:`escpos.escpos.Escpos.text`.
    The return code for this exception is `50`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.TextError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize TextError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 50

    def __str__(self) -> str:
        """Return string representation of TextError."""
        return f"Text string must be supplied to the text() method ({self.msg})"


class CashDrawerError(Error):
    """Valid pin must be set in order to send pulse.

    A valid pin number has to be passed onto the method :py:meth:`escpos.escpos.Escpos.cashdraw`.
    The return code for this exception is `60`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.CashDrawerError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize CashDrawerError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 60

    def __str__(self) -> str:
        """Return string representation of CashDrawerError."""
        return f"Valid pin must be set to send pulse ({self.msg})"


class TabPosError(Error):
    """Tab position is invalid.

    Valid tab positions must be set by using from 1 to 32 tabs, and between 1 and 255 tab size values.
    Both values multiplied must not exceed 255, since it is the maximum tab value.

    This exception is raised by :py:meth:`escpos.escpos.Escpos.control`.
    The return code for this exception is `70`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.TabPosError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize TabPosError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 70

    def __str__(self) -> str:
        """Return string representation of TabPosError."""
        return f"Valid tab positions must be in the range 0 to 16 ({self.msg})"


class CharCodeError(Error):
    """Valid char code must be set.

    The supplied charcode-name in :py:meth:`escpos.escpos.Escpos.charcode` is unknown.
    The return code for this exception is `80`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.CharCodeError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize CharCodeError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 80

    def __str__(self) -> str:
        """Return string representation of CharCodeError."""
        return f"Valid char code must be set ({self.msg})"


class DeviceNotFoundError(Error):
    """Device was not found.

    The device seems to be not accessible.
    The return code for this exception is `90`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.Error
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize DeviceNotFoundError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 90

    def __str__(self) -> str:
        """Return string representation of DeviceNotFoundError."""
        return f"Device not found ({self.msg})"


class USBNotFoundError(DeviceNotFoundError):
    """USB device was not found (probably not plugged in).

    The USB device seems to be not plugged in.
    The return code for this exception is `91`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.USBNotFoundError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize USBNotFoundError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 91

    def __str__(self) -> str:
        """Return string representation of USBNotFoundError."""
        return f"USB device not found ({self.msg})"


class SetVariableError(Error):
    """A set method variable was out of range.

    Check set variables against minimum and maximum values
    The return code for this exception is `100`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.SetVariableError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize SetVariableError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 100

    def __str__(self) -> str:
        """Return string representation of SetVariableError."""
        return f"Set variable out of range ({self.msg})"


# Configuration errors


class ConfigNotFoundError(Error):
    """The configuration file was not found.

    The default or passed configuration file could not be read
    The return code for this exception is `200`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.ConfigNotFoundError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize ConfigNotFoundError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 200

    def __str__(self) -> str:
        """Return string representation of ConfigNotFoundError."""
        return f"Configuration not found ({self.msg})"


class ConfigSyntaxError(Error):
    """The configuration file is invalid.

    The syntax is incorrect
    The return code for this exception is `210`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.ConfigSyntaxError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize ConfigSyntaxError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 210

    def __str__(self) -> str:
        """Return string representation of ConfigSyntaxError."""
        return f"Configuration syntax is invalid ({self.msg})"


class ConfigSectionMissingError(Error):
    """The configuration file is missing a section.

    The part of the config asked for does not exist in the loaded configuration
    The return code for this exception is `220`.

    inheritance:

    .. inheritance-diagram:: escpos.exceptions.ConfigSectionMissingError
        :parts: 1

    """

    def __init__(self, msg: str = "") -> None:
        """Initialize ConfigSectionMissingError object."""
        Error.__init__(self, msg)
        self.msg = msg
        self.resultcode = 220

    def __str__(self) -> str:
        """Return string representation of ConfigSectionMissingError."""
        return f"Configuration section is missing ({self.msg})"
