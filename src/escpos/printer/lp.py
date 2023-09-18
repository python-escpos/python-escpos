#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the LP printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""

import functools
import logging
import subprocess
import sys
from typing import ByteString

from ..escpos import Escpos
from ..exceptions import DeviceNotFoundError


def is_usable() -> bool:
    """Indicate whether this component can be used due to dependencies."""
    usable = False
    if not sys.platform.startswith("win"):
        usable = True
    return usable


def dependency_linux_lp(func):
    """Indicate dependency on non Windows."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Throw a RuntimeError if not on a non-Windows system."""
        if not is_usable():
            raise RuntimeError(
                "This printer driver depends on LP which is not"
                "available on Windows systems."
            )
        return func(*args, **kwargs)

    return wrapper


class LP(Escpos):
    """Simple UNIX lp command raw printing.

    Thanks to `Oyami-Srk comment <https://github.com/python-escpos/python-escpos/pull/348#issuecomment-549558316>`_.

    inheritance:

    .. inheritance-diagram:: escpos.printer.LP
        :parts: 1

    """

    @staticmethod
    def is_usable() -> bool:
        """Indicate whether this printer class is usable.

        Will return True if dependencies are available.
        Will return False if not.
        """
        return is_usable()

    def __init__(self, printer_name: str = "", *args, **kwargs):
        """LP class constructor.

        :param printer_name: CUPS printer name (Optional)
        :param auto_flush: Automatic flush after every _raw() (Optional)
        :type auto_flush: bool
        """
        Escpos.__init__(self, *args, **kwargs)
        self.printer_name = printer_name
        self.auto_flush = kwargs.get("auto_flush", True)

    @dependency_linux_lp
    def open(self, raise_not_found: bool = True) -> None:
        """Invoke _lp_ in a new subprocess and wait for commands.

        By default raise an exception if device is not found.

        :param raise_not_found: Default True.
                                False to log error but do not raise exception.

        :raises: :py:exc:`~escpos.exceptions.DeviceNotFoundError`
        """
        if self._device:
            self.close()

        # Open device
        self.device = subprocess.Popen(
            ["lp", "-d", self.printer_name, "-o", "raw"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

        error: ByteString = b""
        if self.device and self.device.stderr:
            error = self.device.stderr.read()
        if bool(error):
            # Raise exception or log error and cancel
            self.device = None
            if raise_not_found:
                raise DeviceNotFoundError(
                    f"Unable to start a print job for the printer {self.printer_name}:"
                    + f"\n{error!r}"
                )
            else:
                logging.error("LP printing %s not available", self.printer_name)
                return
        logging.info("LP printer enabled")

    def close(self):
        """Stop the subprocess."""
        if not self._device:
            return
        logging.info("Closing LP connection to printer %s", self.printer_name)
        self.device.terminate()
        self._device = False

    def flush(self):
        """End line and wait for new commands."""
        if self.device.stdin.writable():
            self.device.stdin.write(b"\n")
        if self.device.stdin.closed is False:
            self.device.stdin.close()
        self.device.wait()
        self.open()

    def _raw(self, msg):
        """Write raw command(s) to the printer.

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        if self.device.stdin.writable():
            self.device.stdin.write(msg)
        else:
            raise Exception("Not a valid pipe for lp process")
        if self.auto_flush:
            self.flush()
