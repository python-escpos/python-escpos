#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the Win32Raw printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""

import functools
import logging
from typing import Any, Literal, Optional, Union

from ..escpos import Escpos
from ..exceptions import DeviceNotFoundError

#: keeps track if the win32print dependency could be loaded (:py:class:`escpos.printer.Win32Raw`)
_DEP_WIN32PRINT = False


try:
    import pywintypes
    import win32print

    _DEP_WIN32PRINT = True
    PyPrinterHANDLE: Any = win32print.OpenPrinter
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
    def __init__(self, printer_name: str = "", *args, **kwargs) -> None:
        """Initialize default printer."""
        Escpos.__init__(self, *args, **kwargs)
        self.printer_name = printer_name
        self.job_name = ""

        self._device: Union[
            Literal[False],
            Literal[None],
            "PyPrinterHANDLE",
        ] = False

    @property
    def printers(self) -> dict:
        """Available Windows printers."""
        return {
            printer["pPrinterName"]: printer
            for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_NAME, "", 4)
        }

    def open(
        self, job_name: str = "python-escpos", raise_not_found: bool = True
    ) -> None:
        """Open connection to default printer.

        By default raise an exception if device is not found.

        :param raise_not_found: Default True.
                                False to log error but do not raise exception.

        :raises: :py:exc:`~escpos.exceptions.DeviceNotFoundError`
        """
        if self._device:
            self.close()

        self.job_name = job_name
        try:
            # Name validation, set default if no given name
            self.printer_name = self.printer_name or win32print.GetDefaultPrinter()
            assert self.printer_name in self.printers, "Incorrect printer name"
            # Open device
            self.device: Optional["PyPrinterHANDLE"] = win32print.OpenPrinter(
                self.printer_name
            )
            if self.device:
                self.current_job = win32print.StartDocPrinter(
                    self.device, 1, (job_name, "", "RAW")
                )
                win32print.StartPagePrinter(self.device)
        except (AssertionError, pywintypes.error) as e:
            # Raise exception or log error and cancel
            self.device = None
            if raise_not_found:
                raise DeviceNotFoundError(
                    f"Unable to start a print job for the printer {self.printer_name}:"
                    + f"\n{e}"
                )
            else:
                logging.error("Win32Raw printing %s not available", self.printer_name)
                return
        logging.info("Win32Raw printer enabled")

    def close(self) -> None:
        """Close connection to default printer."""
        if self._device is False or self._device is None:  # Literal False | None
            return
        logging.info("Closing Win32Raw connection to printer %s", self.printer_name)
        win32print.EndPagePrinter(self._device)
        win32print.EndDocPrinter(self._device)
        win32print.ClosePrinter(self._device)
        self._device = False

    def _raw(self, msg: bytes) -> None:
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        """
        if self.printer_name is None:
            raise DeviceNotFoundError("Printer not found")
        if not self.device:
            raise DeviceNotFoundError("Printer job not opened")
        win32print.WritePrinter(self.device, msg)  # type: ignore

        # there is a bug in the typeshed
        # https://github.com/mhammond/pywin32/blob/main/win32/src/win32print/win32print.cpp#L976
        # https://github.com/python/typeshed/blob/main/stubs/pywin32/win32/win32print.pyi#L27C4-L27C4
