#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the Serial printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""


import functools
import logging
from typing import Literal, Optional, Union

from ..escpos import Escpos
from ..exceptions import DeviceNotFoundError

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
        devfile: str = "",
        baudrate: int = 9600,
        bytesize: int = 8,
        timeout: Union[int, float] = 1,
        parity: Optional[str] = None,
        stopbits: Optional[int] = None,
        xonxoff: bool = False,
        dsrdtr: bool = True,
        *args,
        **kwargs,
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

        self._device: Union[Literal[False], Literal[None], serial.Serial] = False

    @dependency_pyserial
    def open(self, raise_not_found: bool = True) -> None:
        """Set up serial port and set is as escpos device.

        By default raise an exception if device is not found.

        :param raise_not_found: Default True.
                                False to log error but do not raise exception.

        :raises: :py:exc:`~escpos.exceptions.DeviceNotFoundError`
        """
        if self._device:
            if self.device and self.device.is_open:
                self.close()

        try:
            # Open device
            self.device: Optional[serial.Serial] = serial.Serial(
                port=self.devfile,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                timeout=self.timeout,
                xonxoff=self.xonxoff,
                dsrdtr=self.dsrdtr,
            )
        except (ValueError, serial.SerialException) as e:
            # Raise exception or log error and cancel
            self.device = None
            if raise_not_found:
                raise DeviceNotFoundError(
                    f"Unable to open serial printer on {self.devfile}:\n{e}"
                )
            else:
                logging.error("Serial device %s not found", self.devfile)
                return
        logging.info("Serial printer enabled")

    def _raw(self, msg: bytes) -> None:
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        """
        assert self.device
        self.device.write(msg)

    def _read(self) -> bytes:
        """Read the data buffer and return it to the caller."""
        assert self.device
        return self.device.read(16)

    def close(self) -> None:
        """Close Serial interface."""
        if not self._device:
            return
        logging.info("Closing Serial connection to printer %s", self.devfile)
        if self._device and self._device.is_open:
            self._device.flush()
            self._device.close()
        self._device = False
