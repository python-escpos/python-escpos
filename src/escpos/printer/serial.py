#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the CupsPrinter printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""


import functools

from ..escpos import Escpos

#: keeps track if the pyserial dependency could be loaded (:py:class:`escpos.printer.Serial`)
_DEP_PYSERIAL = False

try:
    import serial

    _DEP_PYSERIAL = True
except ImportError:
    pass


def is_usable() -> bool:
    """Indicate whether this component can be used due to dependencies."""
    usable = False
    if _DEP_PYSERIAL:
        usable = True
    return usable


def dependency_pyserial(func):
    """Indicate dependency on pyserial."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Throw a RuntimeError if pyserial not installed."""
        if not is_usable():
            raise RuntimeError(
                "Printing with Serial requires the pyserial library to"
                "be installed. Please refer to the documentation on"
                "what to install and install the dependencies for pyserial."
            )
        return func(*args, **kwargs)

    return wrapper


class Serial(Escpos):
    """Serial printer.

    This class describes a printer that is connected by serial interface.

    inheritance:

    .. inheritance-diagram:: escpos.printer.Serial
        :parts: 1

    """

    @staticmethod
    def is_usable() -> bool:
        """Indicate whether this printer class is usable.

        Will return True if dependencies are available.
        Will return False if not.
        """
        return is_usable()

    @dependency_pyserial
    def __init__(
        self,
        devfile="/dev/ttyS0",
        baudrate=9600,
        bytesize=8,
        timeout=1,
        parity=None,
        stopbits=None,
        xonxoff=False,
        dsrdtr=True,
        *args,
        **kwargs
    ):
        """Initialize serial printer.

        :param devfile:  Device file under dev filesystem
        :param baudrate: Baud rate for serial transmission
        :param bytesize: Serial buffer size
        :param timeout:  Read/Write timeout
        :param parity:   Parity checking
        :param stopbits: Number of stop bits
        :param xonxoff:  Software flow control
        :param dsrdtr:   Hardware flow control (False to enable RTS/CTS)
        """
        Escpos.__init__(self, *args, **kwargs)
        self.devfile = devfile
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.timeout = timeout
        if parity:
            self.parity = parity
        else:
            self.parity = serial.PARITY_NONE
        if stopbits:
            self.stopbits = stopbits
        else:
            self.stopbits = serial.STOPBITS_ONE
        self.xonxoff = xonxoff
        self.dsrdtr = dsrdtr

        self.open()

    @dependency_pyserial
    def open(self):
        """Set up serial port and set is as escpos device."""
        if self.device is not None and self.device.is_open:
            self.close()
        self.device = serial.Serial(
            port=self.devfile,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits,
            timeout=self.timeout,
            xonxoff=self.xonxoff,
            dsrdtr=self.dsrdtr,
        )

        if self.device is not None:
            print("Serial printer enabled")
        else:
            print("Unable to open serial printer on: {0}".format(str(self.devfile)))

    def _raw(self, msg):
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        self.device.write(msg)

    def _read(self):
        """Read the data buffer and return it to the caller."""
        return self.device.read(16)

    def close(self):
        """Close Serial interface."""
        if self.device is not None and self.device.is_open:
            self.device.flush()
            self.device.close()
