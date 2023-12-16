#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the CupsPrinter printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""

import functools
import logging
import tempfile
from typing import Literal, Optional, Type, Union

from ..escpos import Escpos
from ..exceptions import DeviceNotFoundError

#: keeps track if the pycups dependency could be loaded (:py:class:`escpos.printer.CupsPrinter`)
_DEP_PYCUPS = False

try:
    import cups

    _DEP_PYCUPS = True
    # Store server defaults before further configuration
    DEFAULT_HOST = cups.getServer()
    DEFAULT_PORT = cups.getPort()
except ImportError:
    pass


# TODO: dev build mode that let's the wrapper bypass?


def is_usable() -> bool:
    """Indicate whether this component can be used due to dependencies."""
    usable = False
    if _DEP_PYCUPS:
        usable = True
    return usable


def dependency_pycups(func):
    """Indicate dependency on pycups."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Throw a RuntimeError if pycups is not imported."""
        if not is_usable():
            raise RuntimeError(
                "Printing with PyCups requires the pycups library to"
                "be installed. Please refer to the documentation on"
                "what to install and install the dependencies for pycups."
            )
        return func(*args, **kwargs)

    return wrapper


class CupsPrinter(Escpos):
    """Simple CUPS printer connector.

    .. note::

        Requires ``pycups`` which in turn needs the cups development library package:
            - Ubuntu/Debian: ``libcups2-dev``
            - OpenSuse/Fedora: ``cups-devel``

    inheritance:

    .. inheritance-diagram:: escpos.printer.CupsPrinter
        :parts: 1

    """

    @staticmethod
    def is_usable() -> bool:
        """Indicate whether this printer class is usable.

        Will return True if dependencies are available.
        Will return False if not.
        """
        return is_usable()

    @dependency_pycups
    def __init__(self, printer_name: str = "", *args, **kwargs) -> None:
        """Class constructor for CupsPrinter.

        :param printer_name: CUPS printer name (Optional)
        :param host: CUPS server host/ip (Optional)
        :type host: str
        :param port: CUPS server port (Optional)
        :type port: int
        """
        Escpos.__init__(self, *args, **kwargs)
        self.host, self.port = args or (
            kwargs.get("host", DEFAULT_HOST),
            kwargs.get("port", DEFAULT_PORT),
        )
        self.tmpfile = tempfile.NamedTemporaryFile(delete=True)
        self.printer_name = printer_name
        self.job_name = ""
        self.pending_job = False

        self._device: Union[
            Literal[False], Literal[None], Type[cups.Connection]
        ] = False

    @property
    def printers(self) -> dict:
        """Available CUPS printers."""
        if self.device:
            return self.device.getPrinters()
        return {}

    def open(
        self, job_name: str = "python-escpos", raise_not_found: bool = True
    ) -> None:
        """Set up a new print job and target the printer.

        A call to this method is required to send new jobs to
        the CUPS connection after close.

        Defaults to default CUPS printer.
        Creates a new temporary file buffer.

        By default raise an exception if device is not found.

        :param raise_not_found: Default True.
                                False to log error but do not raise exception.

        :raises: :py:exc:`~escpos.exceptions.DeviceNotFoundError`
        """
        if self._device:
            self.close()

        cups.setServer(self.host)
        cups.setPort(self.port)
        self.job_name = job_name
        if self.tmpfile.closed:
            self.tmpfile = tempfile.NamedTemporaryFile(delete=True)

        try:
            # Open device
            self.device: Optional[Type[cups.Connection]] = cups.Connection()
            if self.device:
                # Name validation, set default if no given name
                self.printer_name = self.printer_name or self.device.getDefault()
                assert self.printer_name in self.printers, "Incorrect printer name"
        except (RuntimeError, AssertionError) as e:
            # Raise exception or log error and cancel
            self.device = None
            if raise_not_found:
                raise DeviceNotFoundError(
                    f"Unable to start a print job for the printer {self.printer_name}:"
                    + f"\n{e}"
                )
            else:
                logging.error(
                    "CupsPrinter printing %s not available", self.printer_name
                )
                return
        logging.info("CupsPrinter printer enabled")

    def _raw(self, msg: bytes) -> None:
        """Append any command sent in raw format to temporary file.

        :param msg: arbitrary code to be printed
        """
        self.pending_job = True
        try:
            self.tmpfile.write(msg)
        except TypeError:
            self.pending_job = False
            raise TypeError("Bytes required. Printer job not opened")

    def send(self) -> None:
        """Send the print job to the printer."""
        assert self.device
        if self.pending_job:
            # Rewind tempfile
            self.tmpfile.seek(0)
            # Print temporary file via CUPS printer.
            self.device.printFile(
                self.printer_name,
                self.tmpfile.name,
                self.job_name,
                {"document-format": cups.CUPS_FORMAT_RAW},
            )
        self._clear()

    def _clear(self) -> None:
        """Finish the print job.

        Remove temporary file.
        """
        self.tmpfile.close()
        self.pending_job = False

    def _read(self) -> bytes:
        """Return a single-item array with the accepting state of the print queue.

        states: idle = [3], printing a job = [4], stopped = [5]
        """
        printer = self.printers.get(self.printer_name, {})
        state = printer.get("printer-state")
        if not state or state in [4, 5]:
            return b"8"  # offline
        return b"0"  # online

    def close(self) -> None:
        """Close CUPS connection.

        Send pending job to the printer if needed.
        """
        if not self._device:
            return
        if self.pending_job:
            self.send()
        logging.info("Closing CUPS connection to printer %s", self.printer_name)
        self._device = False
