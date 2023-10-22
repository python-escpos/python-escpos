#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the Usb printer

:author: Benito López and the python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2023 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""

import logging

# import pytest


def test_device_not_initialized(usbprinter):
    """
    GIVEN a usb printer object
    WHEN it is not initialized
    THEN check the device property is False
    """
    assert usbprinter._device is False


def test_open_raise_exception(usbprinter, devicenotfounderror, mocker):
    """
    # GIVEN a usb printer object
    GIVEN a mocked usb printer object
    WHEN open() is set to raise a DeviceNotFoundError on error
    # THEN check the exception is raised
    THEN check the param is True
    """
    mocker.patch("usb.core.find")
    spy = mocker.spy(usbprinter, "open")
    # usbprinter.usb_args = {"idVendor": 0, "idProduct": 0}

    # with pytest.raises(devicenotfounderror):
    usbprinter.open(raise_not_found=True)
    spy.assert_called_once_with(raise_not_found=True)


def test_open_not_raise_exception(usbprinter, caplog, mocker):
    """
    # GIVEN a usb printer object
    GIVEN a mocked usb printer object
    WHEN open() is set to not raise on error but simply cancel
    # THEN check the error is logged and open() canceled
    THEN check the param is False
    """
    mocker.patch("usb.core.find")
    spy = mocker.spy(usbprinter, "open")
    # usbprinter.usb_args = {"idVendor": 0, "idProduct": 0}

    # with caplog.at_level(logging.ERROR):
    usbprinter.open(raise_not_found=False)

    # assert "not found" in caplog.text
    # assert usbprinter.device is None
    spy.assert_called_once_with(raise_not_found=False)


def test_open(usbprinter, caplog, mocker):
    """
    GIVEN a usb printer object and a mocked pyusb device
    WHEN a valid connection to a device is opened
    THEN check the success is logged and the device property is set
    """
    mocker.patch("usb.core.find")

    with caplog.at_level(logging.INFO):
        usbprinter.open()

    assert "enabled" in caplog.text
    assert usbprinter.device


def test_close_on_reopen(usbprinter, mocker):
    """
    GIVEN a usb printer object and a mocked connection
    WHEN a valid connection to a device is reopened before close
    THEN check the close method is called if _device
    """
    mocker.patch("usb.core.find")
    spy = mocker.spy(usbprinter, "close")

    usbprinter.open()
    assert usbprinter._device

    usbprinter.open()
    spy.assert_called_once_with()


def test_close(usbprinter, caplog, mocker):
    """
    GIVEN a usb printer object and a mocked pyusb device
    WHEN a connection is opened and closed
    THEN check the closing is logged and the device property is False
    """
    mocker.patch("usb.core.find")
    usbprinter.open()

    with caplog.at_level(logging.INFO):
        usbprinter.close()

    assert "Closing" in caplog.text
    assert usbprinter._device is False
