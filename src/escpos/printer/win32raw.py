#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the CupsPrinter printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""

from ..escpos import Escpos

_WIN32PRINT = False
try:
    import win32print

    _WIN32PRINT = True
except ImportError:
    pass


if _WIN32PRINT:

    class Win32Raw(Escpos):
        """Printer binding for win32 API.

        Uses the module pywin32 for printing.

        inheritance:

        .. inheritance-diagram:: escpos.printer.Win32Raw
            :parts: 1

        """

        def __init__(self, printer_name=None, *args, **kwargs):
            """Initialize default printer."""
            Escpos.__init__(self, *args, **kwargs)
            if printer_name is not None:
                self.printer_name = printer_name
            else:
                self.printer_name = win32print.GetDefaultPrinter()
            self.hPrinter = None
            self.open()

        def open(self, job_name="python-escpos"):
            """Open connection to default printer."""
            if self.printer_name is None:
                raise Exception("Printer not found")
            self.hPrinter = win32print.OpenPrinter(self.printer_name)
            self.current_job = win32print.StartDocPrinter(
                self.hPrinter, 1, (job_name, None, "RAW")
            )
            win32print.StartPagePrinter(self.hPrinter)

        def close(self):
            """Close connection to default printer."""
            if not self.hPrinter:
                return
            win32print.EndPagePrinter(self.hPrinter)
            win32print.EndDocPrinter(self.hPrinter)
            win32print.ClosePrinter(self.hPrinter)
            self.hPrinter = None

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
