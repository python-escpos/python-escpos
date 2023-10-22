#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the Serial printer

:author: Benito López and the python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2023 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""

import logging

import pytest


def test_device_not_initialized(serialprinter):
    """
    GIVEN a serial printer object
    WHEN it is not initialized
    THEN check the device property is False
    """
    assert serialprinter._device is False


def test_open_raise_exception(serialprinter, devicenotfounderror):
    """
    GIVEN a serial printer object
    WHEN open() is set to raise a DeviceNotFoundError on error
    THEN check the exception is raised
    """
    serialprinter.devfile = "fake/device"

    with pytest.raises(devicenotfounderror):
        serialprinter.open(raise_not_found=True)


def test_open_not_raise_exception(serialprinter, caplog):
    """
    GIVEN a serial printer object
    WHEN open() is set to not raise on error but simply cancel
    THEN check the error is logged and open() canceled
    """
    serialprinter.devfile = "fake/device"

    with caplog.at_level(logging.ERROR):
        serialprinter.open(raise_not_found=False)

    assert "not found" in caplog.text
    assert serialprinter.device is None


def test_open(serialprinter, caplog, mocker):
    """
    GIVEN a serial printer object and a mocked pyserial device
    WHEN a valid connection to a device is opened
    THEN check the success is logged and the device property is set
    """
    mocker.patch("serial.Serial")

    with caplog.at_level(logging.INFO):
        serialprinter.open()

    assert "enabled" in caplog.text
    assert serialprinter.device


def test_close_on_reopen(serialprinter, mocker):
    """
    GIVEN a serial printer object and a mocked connection
    WHEN a valid connection to a device is reopened before close
    THEN check the close method is called if _device
    """
    mocker.patch("serial.Serial")
    spy = mocker.spy(serialprinter, "close")

    serialprinter.open()
    assert serialprinter._device

    serialprinter.open()
    spy.assert_called_once_with()


def test_close(serialprinter, caplog, mocker):
    """
    GIVEN a serial printer object and a mocked pyserial device
    WHEN a connection is opened and closed
    THEN check the closing is logged and the device property is False
    """
    mocker.patch("serial.Serial")
    serialprinter.open()

    with caplog.at_level(logging.INFO):
        serialprinter.close()

    assert "Closing" in caplog.text
    assert serialprinter._device is False
