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

#: keeps track if the win32print dependency could be loaded (:py:class:`escpos.printer.Win32Raw`)
_DEP_WIN32PRINT = False

try:
    import win32print

    _DEP_WIN32PRINT = True
except ImportError:
    pass


def is_usable() -> bool:
    """Indicate whether this component can be used due to dependencies."""
    usable = False
    if _DEP_WIN32PRINT:
        usable = True
    return usable


def dependency_win32print(func):
    """Indicate dependency on win32print."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Throw a RuntimeError if win32print not installed."""
        if not is_usable():
            raise RuntimeError(
                "Printing with Win32Raw requires a win32print library to"
                "be installed. Please refer to the documentation on"
                "what to install and install the dependencies for win32print."
            )
        return func(*args, **kwargs)

    return wrapper


class Win32Raw(Escpos):
    """Printer binding for win32 API.

    Uses the module pywin32 for printing.

    inheritance:

    .. inheritance-diagram:: escpos.printer.Win32Raw
        :parts: 1

    """

    @staticmethod
    def is_usable() -> bool:
        """Indicate whether this printer class is usable.

        Will return True if dependencies are available.
        Will return False if not.
        """
        return is_usable()

    @dependency_win32print
    def __init__(self, printer_name=None, *args, **kwargs):
        """Initialize default printer."""
        Escpos.__init__(self, *args, **kwargs)
        if printer_name is not None:
            self.printer_name = printer_name
        else:
            self.printer_name = win32print.GetDefaultPrinter()
        self.hPrinter = None
        self.open()

    @dependency_win32print
    def open(self, job_name="python-escpos"):
        """Open connection to default printer."""
        if self.printer_name is None:
            raise Exception("Printer not found")
        self.hPrinter = win32print.OpenPrinter(self.printer_name)
        self.current_job = win32print.StartDocPrinter(
            self.hPrinter, 1, (job_name, None, "RAW")
        )
        win32print.StartPagePrinter(self.hPrinter)

    @dependency_win32print
    def close(self):
        """Close connection to default printer."""
        if not self.hPrinter:
            return
        win32print.EndPagePrinter(self.hPrinter)
        win32print.EndDocPrinter(self.hPrinter)
        win32print.ClosePrinter(self.hPrinter)
        self.hPrinter = None

    @dependency_win32print
    def _raw(self, msg):
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        if self.printer_name is None:
            raise Exception("Printer not found")
        if self.hPrinter is None:
            raise Exception("Printer job not opened")
        win32print.WritePrinter(self.hPrinter, msg)
