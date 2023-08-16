#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the CupsPrinter printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""

from ..escpos import Escpos


def is_usable() -> bool:
    """Indicate whether this component can be used due to dependencies."""
    return True


class File(Escpos):
    """Generic file printer.

    This class is used for parallel port printer or other printers that are directly attached to the filesystem.
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

    def __init__(self, devfile="/dev/usb/lp0", auto_flush=True, *args, **kwargs):
        """Initialize file printer with device file.

        :param devfile: Device file under dev filesystem
        :param auto_flush: automatically call flush after every call of _raw()
        """
        Escpos.__init__(self, *args, **kwargs)
        self.devfile = devfile
        self.auto_flush = auto_flush
        self.open()

    def open(self):
        """Open system file."""
        self.device = open(self.devfile, "wb")

        if self.device is None:
            print("Could not open the specified file {0}".format(self.devfile))

    def flush(self):
        """Flush printing content."""
        self.device.flush()

    def _raw(self, msg):
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        self.device.write(msg)
        if self.auto_flush:
            self.flush()

    def close(self):
        """Close system file."""
        if self.device is not None:
            self.device.flush()
            self.device.close()
