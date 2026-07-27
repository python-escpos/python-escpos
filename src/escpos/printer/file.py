#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the File printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""

import logging
import os
import time
from typing import IO, Literal, Optional, Union

from ..escpos import Escpos
from ..exceptions import DeviceNotFoundError


def is_usable() -> bool:
    """Indicate whether this component can be used due to dependencies."""
    return True


class File(Escpos):
    """Generic file printer.

    This class is used for parallel port printer or other printers that are directly attached to the file system.
    Note that you should stay away from using USB-to-Parallel-Adapter since they are unreliable
    and produce arbitrary errors.

    inheritance:

    .. inheritance-diagram:: escpos.printer.File
        :parts: 1

    """

    @staticmethod
    def is_usable() -> bool:
        """Indicate whether this printer class is usable.

        Will return True if dependencies are available.
        Will return False if not.
        """
        return is_usable()

    def __init__(self, devfile: str = "", auto_flush: bool = True, *args, **kwargs):
        """Initialize file printer with device file.

        :param devfile: Device file under dev file system
        :param auto_flush: automatically call flush after every call of _raw()
        """
        Escpos.__init__(self, *args, **kwargs)
        self.devfile = devfile
        self.auto_flush = auto_flush

        self._device: Union[Literal[False], Literal[None], IO[bytes]] = False
        self._fd: Optional[int] = None

    def open(self, raise_not_found: bool = True) -> None:
        """Open system file.

        By default raise an exception if device is not found.

        :param raise_not_found: Default True.
                                False to log error but do not raise exception.

        :raises: :py:exc:`~escpos.exceptions.DeviceNotFoundError`
        """
        if self._device:
            self.close()

        try:
            # Open device
            self._fd = os.open(self.devfile, os.O_RDWR)
            self.device: Optional[IO[bytes]] = os.fdopen(self._fd, "wb")
        except OSError as e:
            # Raise exception or log error and cancel
            self.device = None
            if raise_not_found:
                raise DeviceNotFoundError(
                    f"Could not open the specified file {self.devfile}:\n{e}"
                )
            else:
                logging.error("File printer %s not found", self.devfile)
                return
        logging.info("File printer enabled")

    def flush(self) -> None:
        """Flush printing content."""
        if self.device:
            self.device.flush()

    def _raw(self, msg: bytes) -> None:
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        """
        assert self.device
        self.device.write(msg)
        if self.auto_flush:
            self.flush()

    def _read(self) -> bytes:
        """Read a data buffer and return it to the caller."""
        assert self.device and not self.device.closed
        assert self._fd is not None
        if not self.auto_flush:
            logging.warning(
                "Param 'auto_flush' is disabled. Forcing a flush before attempting to read the data"
            )
            self.flush()
        time.sleep(0.2)  # Give some time to respond
        os.lseek(self._fd, -1, os.SEEK_END)  # Rewind 1 byte
        return os.read(self._fd, 16)

    def close(self) -> None:
        """Close system file."""
        if not self._device:
            return
        logging.info("Closing File connection to printer %s", self.devfile)
        if not self.auto_flush:
            self.flush()
        self._device.close()  # This closes also the file descriptor
        self._device = False
