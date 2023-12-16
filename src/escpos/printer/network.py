#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the Network printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""

import logging
import socket
from typing import Literal, Optional, Union

from ..escpos import Escpos
from ..exceptions import DeviceNotFoundError


def is_usable() -> bool:
    """Indicate whether this component can be used due to dependencies."""
    return True


class Network(Escpos):
    """Network printer.

    This class is used to attach to a networked printer.
    You can also use this in order to attach to a printer that
    is forwarded with ``socat``.

    If you have a local printer on parallel port ``/dev/usb/lp0``
    then you could start ``socat`` with:

    .. code-block:: none

        socat -u TCP4-LISTEN:4242,reuseaddr,fork OPEN:/dev/usb/lp0

    Then you should be able to attach to port ``4242`` with this class.
    Otherwise the normal use case would be to have a printer with
    Ethernet interface.
    This type of printer should work the same with this class.
    For the address of the printer check its manuals.

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
        host: str = "",
        port: int = 9100,
        timeout: Union[int, float] = 60,
        *args,
        **kwargs,
    ):
        """Initialize network printer.

        :param host:    Printer's host name or IP address
        :param port:    Port to write to
        :param timeout: timeout in seconds for the socket-library
        """
        Escpos.__init__(self, *args, **kwargs)
        self.host = host
        self.port = port
        self.timeout = timeout

        self._device: Union[Literal[False], Literal[None], socket.socket] = False

    def open(self, raise_not_found: bool = True) -> None:
        """Open TCP socket with ``socket``-library and set it as escpos device.

        By default raise an exception if device is not found.

        :param raise_not_found: Default True.
                                False to log error but do not raise exception.

        :raises: :py:exc:`~escpos.exceptions.DeviceNotFoundError`
        """
        if self._device:
            self.close()

        try:
            # Open device
            self.device: Optional[socket.socket] = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
            self.device.settimeout(self.timeout)
            self.device.connect((self.host, self.port))
        except OSError as e:
            # Raise exception or log error and cancel
            self.device = None
            if raise_not_found:
                raise DeviceNotFoundError(
                    f"Could not open socket for {self.host}:\n{e}"
                )
            else:
                logging.error("Network device %s not found", self.host)
                return
        logging.info("Network printer enabled")

    def _raw(self, msg: bytes) -> None:
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        """
        assert self.device
        self.device.sendall(msg)

    def _read(self) -> bytes:
        """Read data from the TCP socket."""
        assert self.device
        return self.device.recv(16)

    def close(self) -> None:
        """Close TCP connection."""
        if not self._device:
            return
        logging.info("Closing Network connection to printer %s", self.host)
        try:
            self._device.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self._device.close()
        self._device = False
