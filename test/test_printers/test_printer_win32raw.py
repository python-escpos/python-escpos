#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the Win32Raw printer

:author: Benito López and the python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2023 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""

import logging
import sys

import pytest

# skip all the tests if the platform is not Windows
pytestmark = pytest.mark.skipif(
    sys.platform != "win32", reason="Skipping Windows platform specific tests"
)


def test_device_not_initialized(win32rawprinter, mocker):
    """
    GIVEN a win32raw printer object
    WHEN it is not initialized
    THEN check the device property is False
    """
    mocker.patch("win32print.__init__")
    assert win32rawprinter._device is False


def test_open_raise_exception(win32rawprinter, devicenotfounderror, mocker):
    """
    GIVEN a win32raw printer object and a mocked win32printer device
    WHEN open() is set to raise a DeviceNotFoundError on error
    THEN check the exception is raised
    """
    mocker.patch("win32print.__init__")

    win32rawprinter.printer_name = "fake_printer"

    with pytest.raises(devicenotfounderror):
        win32rawprinter.open(raise_not_found=True)


def test_open_not_raise_exception(win32rawprinter, caplog, mocker):
    """
    GIVEN a win32raw printer object and a mocked win32printer device
    WHEN open() is set to not raise on error but simply cancel
    THEN check the error is logged and open() canceled
    """
    mocker.patch("win32print.__init__")

    win32rawprinter.printer_name = "fake_printer"

    with caplog.at_level(logging.ERROR):
        win32rawprinter.open(raise_not_found=False)

    assert "not available" in caplog.text
    assert win32rawprinter.device is None


def test_open(win32rawprinter, caplog, mocker):
    """
    GIVEN a win32raw printer object and a mocked win32printer device
    WHEN a valid connection to a device is opened
    THEN check the success is logged and the device property is set
    """
    mocker.patch("win32print.__init__")

    with caplog.at_level(logging.INFO):
        win32rawprinter.open()

    assert "enabled" in caplog.text
    assert win32rawprinter.device


def test_close_on_reopen(win32rawprinter, mocker):
    """
    GIVEN a win32raw printer object and a mocked connection
    WHEN a valid connection to a device is reopened before close
    THEN check the close method is called if _device
    """
    mocker.patch("win32print.__init__")
    spy = mocker.spy(win32rawprinter, "close")

    win32rawprinter.open()
    assert win32rawprinter._device

    win32rawprinter.open()
    spy.assert_called_once_with()


def test_close(win32rawprinter, mocker, caplog):
    """
    GIVEN a win32raw printer object and a mocked win32print device
    WHEN a connection is opened and closed
    THEN check the closing is logged and the device property is False
    """
    mocker.patch("win32print.__init__")

    win32rawprinter.open()
    with caplog.at_level(logging.INFO):
        win32rawprinter.close()

    assert "Closing" in caplog.text
    assert win32rawprinter._device is False
