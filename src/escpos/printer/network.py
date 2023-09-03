#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the CupsPrinter printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""

import socket
from typing import Union

from ..escpos import Escpos


def is_usable() -> bool:
    """Indicate whether this component can be used due to dependencies."""
    return True


class Network(Escpos):
    """Network printer.

    This class is used to attach to a networked printer. You can also use this in order to attach to a printer that
    is forwarded with ``socat``.

    If you have a local printer on parallel port ``/dev/usb/lp0`` then you could start ``socat`` with:

    .. code-block:: none

        socat -u TCP4-LISTEN:4242,reuseaddr,fork OPEN:/dev/usb/lp0

    Then you should be able to attach to port ``4242`` with this class.
    Otherwise the normal usecase would be to have a printer with ethernet interface. This type of printer should
    work the same with this class. For the address of the printer check its manuals.

    inheritance:

    .. inheritance-diagram:: escpos.printer.Network
        :parts: 1

    """

    @staticmethod
    def is_usable() -> bool:
        """Indicate whether this printer class is usable.

        Will return True if dependencies are available.
        Will return False if not.
        """
        return is_usable()

    def __init__(
        self,
        host: str = None,
        port: int = 9100,
        timeout: Union[int, float] = 60,
        *args,
        **kwargs
    ):
        """Initialize network printer.

        :param host:    Printer's hostname or IP address
        :param port:    Port to write to
        :param timeout: timeout in seconds for the socket-library
        """
        Escpos.__init__(self, *args, **kwargs)
        self.host = host
        self.port = port
        self.timeout = timeout

    def open(self):
        """Open TCP socket with ``socket``-library and set it as escpos device."""
        self.device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device.settimeout(self.timeout)
        self.device.connect((self.host, self.port))

        if not self.device:
            print("Could not open socket for {0}".format(self.host))

    def _raw(self, msg):
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        self.device.sendall(msg)

    def _read(self):
        """Read data from the TCP socket."""
        return self.device.recv(16)

    def close(self):
        """Close TCP connection."""
        if not self._device:
            return
        try:
            self.device.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self.device.close()
        self._device = False
