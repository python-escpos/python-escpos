#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the USB printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""
import functools
import logging
from typing import Dict, Literal, Optional, Type, Union

from ..escpos import Escpos
from ..exceptions import DeviceNotFoundError, USBNotFoundError

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
        idVendor: Optional[int] = None,
        idProduct: Optional[int] = None,
        usb_args: Dict[str, Union[str, int]] = {},
        timeout: Union[int, float] = 0,
        in_ep: int = 0x82,
        out_ep: int = 0x01,
        *args,
        **kwargs,
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

        self.usb_args = usb_args or {}
        if idVendor:
            self.usb_args["idVendor"] = idVendor
        if idProduct:
            self.usb_args["idProduct"] = idProduct

        self._device: Union[
            Literal[False], Literal[None], Type[usb.core.Device]
        ] = False

    @dependency_usb
    def open(self, raise_not_found: bool = True) -> None:
        """Search device on USB tree and set it as escpos device.

        By default raise an exception if device is not found.

        :param raise_not_found: Default True.
                                False to log error but do not raise exception.

        :raises: :py:exc:`~escpos.exceptions.DeviceNotFoundError`
        :raises: :py:exc:`~escpos.exceptions.USBNotFoundError`
        """
        if self._device:
            self.close()

        # Open device
        try:
            self.device: Optional[Type[usb.core.Device]] = usb.core.find(
                **self.usb_args
            )
            assert self.device, USBNotFoundError(
                f"Device {tuple(self.usb_args.values())} not found"
                + " or cable not plugged in."
            )
            self._check_driver()
            self._configure_usb()
        except (AssertionError, usb.core.USBError) as e:
            # Raise exception or log error and cancel
            self.device = None
            if raise_not_found:
                raise DeviceNotFoundError(
                    f"Unable to open USB printer on {tuple(self.usb_args.values())}:"
                    + f"\n{e}"
                )
            else:
                logging.error("USB device %s not found", tuple(self.usb_args.values()))
                return
        logging.info("USB printer enabled")

    def _check_driver(self) -> None:
        """Check the driver.

        pyusb has three backends: libusb0, libusb1 and openusb but
        only libusb1 backend implements the methods is_kernel_driver_active()
        and detach_kernel_driver().
        This helps enable this library to work on Windows.
        """
        if self.device and self.device.backend.__module__.endswith("libusb1"):
            check_driver: Optional[bool] = None

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
                        logging.error("Could not detatch kernel driver: %s", str(e))

    def _configure_usb(self) -> None:
        """Configure USB."""
        if not self.device:
            return
        try:
            self.device.set_configuration()
            self.device.reset()
        except usb.core.USBError as e:
            logging.error("Could not set configuration: %s", str(e))

    def _raw(self, msg: bytes) -> None:
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        """
        assert self.device
        self.device.write(self.out_ep, msg, self.timeout)

    def _read(self) -> bytes:
        """Read a data buffer and return it to the caller."""
        assert self.device
        return self.device.read(self.in_ep, 16)

    @dependency_usb
    def close(self) -> None:
        """Release USB interface."""
        if not self._device:
            return
        logging.info(
            "Closing Usb connection to printer %s", tuple(self.usb_args.values())
        )
        usb.util.dispose_resources(self._device)
        self._device = False
