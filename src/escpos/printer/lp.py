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
from typing import Literal, Optional, Union

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

    @dependency_linux_lp
    def __init__(self, printer_name: str = "", *args, **kwargs):
        """LP class constructor.

        :param printer_name: CUPS printer name (Optional)
        :param auto_flush: Automatic flush after every _raw() (Optional)
        :type auto_flush: bool (Defaults False)
        """
        Escpos.__init__(self, *args, **kwargs)
        self.printer_name = printer_name
        self.auto_flush = kwargs.get("auto_flush", False)
        self._flushed = False

        self._device: Union[Literal[False], Literal[None], subprocess.Popen] = False

    @property
    def printers(self) -> dict:
        """Available CUPS printers."""
        p_names = subprocess.run(
            ["lpstat", "-e"],  # Get printer names
            capture_output=True,
            text=True,
        )
        p_devs = subprocess.run(
            ["lpstat", "-v"],  # Get attached devices
            capture_output=True,
            text=True,
        )
        # List and trim output lines
        names = [name for name in p_names.stdout.split("\n") if name]
        devs = [dev for dev in p_devs.stdout.split("\n") if dev]
        # return a dict of {printer name: attached device} pairs
        return {name: dev.split()[-1] for name in names for dev in devs if name in dev}

    def _get_system_default_printer(self) -> str:
        """Return the system's default printer name."""
        p_name = subprocess.run(
            ["lpstat", "-d"],
            capture_output=True,
            text=True,
        )
        name = p_name.stdout.split()[-1]
        if name not in self.printers:
            return ""
        return name

    def open(
        self,
        job_name: str = "python-escpos",
        raise_not_found: bool = True,
        _close_opened: bool = True,
    ) -> None:
        """Invoke _lp_ in a new subprocess and wait for commands.

        By default raise an exception if device is not found.

        :param raise_not_found: Default True.
                                False to log error but do not raise exception.

        :raises: :py:exc:`~escpos.exceptions.DeviceNotFoundError`
        """
        if self._device and _close_opened:
            self.close()

        self._is_closing = False

        self.job_name = job_name
        try:
            # Name validation, set default if no given name
            self.printer_name = self.printer_name or self._get_system_default_printer()
            assert self.printer_name in self.printers, "Incorrect printer name"
            # Open device
            self.device: Optional[subprocess.Popen] = subprocess.Popen(
                ["lp", "-d", self.printer_name, "-t", self.job_name, "-o", "raw"],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except (AssertionError, subprocess.SubprocessError) as e:
            # Raise exception or log error and cancel
            self.device = None
            if raise_not_found:
                raise DeviceNotFoundError(
                    f"Unable to start a print job for the printer {self.printer_name}:"
                    + f"\n{e}"
                )
            else:
                logging.error("LP printing %s not available", self.printer_name)
                return
        logging.info("LP printer enabled")

    def close(self) -> None:
        """Stop the subprocess."""
        if not self._device:
            return
        logging.info("Closing LP connection to printer %s", self.printer_name)
        self._is_closing = True
        if not self.auto_flush:
            self.flush()
        self._device.terminate()
        self._device = False

    def flush(self) -> None:
        """End line and wait for new commands."""
        if not self.device or not self.device.stdin:
            return

        if self._flushed:
            return

        if self.device.stdin.writable():
            self.device.stdin.write(b"\n")
        if self.device.stdin.closed is False:
            self.device.stdin.close()
        self.device.wait()
        self._flushed = True
        if not self._is_closing:
            self.open(_close_opened=False)

    def _raw(self, msg: bytes) -> None:
        """Write raw command(s) to the printer.

        :param msg: arbitrary code to be printed
        """
        assert self.device is not None
        assert self.device.stdin is not None
        if self.device.stdin.writable():
            self.device.stdin.write(msg)
        else:
            raise subprocess.SubprocessError("Not a valid pipe for lp process")
        self._flushed = False
        if self.auto_flush:
            self.flush()
