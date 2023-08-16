#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the USB printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""
import functools

from ..escpos import Escpos
from ..exceptions import USBNotFoundError

#: keeps track if the usb dependency could be loaded (:py:class:`escpos.printer.Usb`)
_DEP_USB = False

try:
    import usb.core
    import usb.util

    _DEP_USB = True
except ImportError:
    pass


def is_usable() -> bool:
    """Indicate whether this component can be used due to dependencies."""
    usable = False
    if _DEP_USB:
        usable = True
    return usable


def dependency_usb(func):
    """Indicate dependency on usb."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Throw a RuntimeError if usb not installed."""
        if not is_usable():
            raise RuntimeError(
                "Printing with USB connection requires a usb library to"
                "be installed. Please refer to the documentation on"
                "what to install and install the dependencies for USB."
            )
        return func(*args, **kwargs)

    return wrapper


class Usb(Escpos):
    """USB printer.

    This class describes a printer that natively speaks USB.

    inheritance:

    .. inheritance-diagram:: escpos.printer.Usb
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
        idVendor,
        idProduct,
        usb_args=None,
        timeout=0,
        in_ep=0x82,
        out_ep=0x01,
        *args,
        **kwargs
    ):
        """Initialize USB printer.

        :param idVendor: Vendor ID
        :param idProduct: Product ID
        :param usb_args: Optional USB arguments (e.g. custom_match)
        :param timeout: Is the time limit of the USB operation. Default without timeout.
        :param in_ep: Input end point
        :param out_ep: Output end point
        """
        Escpos.__init__(self, *args, **kwargs)
        self.timeout = timeout
        self.in_ep = in_ep
        self.out_ep = out_ep

        usb_args = usb_args or {}
        if idVendor:
            usb_args["idVendor"] = idVendor
        if idProduct:
            usb_args["idProduct"] = idProduct
        self.open(usb_args)

    @dependency_usb
    def open(self, usb_args):
        """Search device on USB tree and set it as escpos device.

        :param usb_args: USB arguments
        """
        self.device = usb.core.find(**usb_args)
        if self.device is None:
            raise USBNotFoundError("Device not found or cable not plugged in.")

        self.idVendor = self.device.idVendor
        self.idProduct = self.device.idProduct

        # pyusb has three backends: libusb0, libusb1 and openusb but
        # only libusb1 backend implements the methods is_kernel_driver_active()
        # and detach_kernel_driver().
        # This helps enable this library to work on Windows.
        if self.device.backend.__module__.endswith("libusb1"):
            check_driver = None

            try:
                check_driver = self.device.is_kernel_driver_active(0)
            except NotImplementedError:
                pass

            if check_driver is None or check_driver:
                try:
                    self.device.detach_kernel_driver(0)
                except NotImplementedError:
                    pass
                except usb.core.USBError as e:
                    if check_driver is not None:
                        print("Could not detatch kernel driver: {0}".format(str(e)))

        try:
            self.device.set_configuration()
            self.device.reset()
        except usb.core.USBError as e:
            print("Could not set configuration: {0}".format(str(e)))

    def _raw(self, msg):
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        self.device.write(self.out_ep, msg, self.timeout)

    def _read(self):
        """Read a data buffer and return it to the caller."""
        return self.device.read(self.in_ep, 16)

    @dependency_usb
    def close(self):
        """Release USB interface."""
        if self.device:
            usb.util.dispose_resources(self.device)
        self.device = None
