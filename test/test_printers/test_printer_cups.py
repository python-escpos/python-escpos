#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the Cups printer

:author: Benito López and the python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2023 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""

import logging
import sys

import pytest

# skip all the tests if the platform is Windows
pytestmark = pytest.mark.skipif(
    sys.platform == "win32", reason="skipping non Windows platform specific tests"
)


def test_device_not_initialized(cupsprinter):
    """
    GIVEN a cups printer object
    WHEN it is not initialized
    THEN check the device property is False
    """
    assert cupsprinter._device is False


def test_open_raise_exception(cupsprinter, devicenotfounderror):
    """
    GIVEN a cups printer object
    WHEN open() is set to raise a DeviceNotFoundError on error
    THEN check the exception is raised
    """
    cupsprinter.host = "fakehost"

    with pytest.raises(devicenotfounderror):
        cupsprinter.open(raise_not_found=True)


def test_open_not_raise_exception(cupsprinter, caplog):
    """
    GIVEN a cups printer object
    WHEN open() is set to not raise on error but simply cancel
    THEN check the error is logged and open() canceled
    """
    cupsprinter.host = "fakehost"

    with caplog.at_level(logging.ERROR):
        cupsprinter.open(raise_not_found=False)

    assert "not available" in caplog.text
    assert cupsprinter.device is None


def test_open(cupsprinter, caplog, mocker):
    """
    GIVEN a cups printer object and a mocked pycups device
    WHEN a valid connection to a device is opened
    THEN check the success is logged and the device property is set
    """
    mocker.patch("cups.Connection")
    mocker.patch("escpos.printer.CupsPrinter.printers", new={"test_printer": "Test"})

    cupsprinter.printer_name = "test_printer"
    assert cupsprinter.printer_name in cupsprinter.printers

    with caplog.at_level(logging.INFO):
        cupsprinter.open()

    assert "enabled" in caplog.text
    assert cupsprinter.device


def test_close_on_reopen(cupsprinter, mocker):
    """
    GIVEN a cups printer object and a mocked connection
    WHEN a valid connection to a device is reopened before close
    THEN check the close method is called if _device
    """
    spy = mocker.spy(cupsprinter, "close")
    mocker.patch("cups.Connection")
    mocker.patch("escpos.printer.CupsPrinter.printers", new={"test_printer": "Test"})

    cupsprinter.printer_name = "test_printer"

    cupsprinter.open()
    assert cupsprinter._device

    cupsprinter.open()
    spy.assert_called_once_with()


def test_close(cupsprinter, caplog, mocker):
    """
    GIVEN a cups printer object and a mocked pycups device
    WHEN a connection is opened and closed
    THEN check the closing is logged and the device property is False
    """
    mocker.patch("cups.Connection")
    mocker.patch("escpos.printer.CupsPrinter.printers", new={"test_printer": "Test"})

    cupsprinter.printer_name = "test_printer"
    cupsprinter.open()

    with caplog.at_level(logging.INFO):
        cupsprinter.close()

    assert "Closing" in caplog.text
    assert cupsprinter._device is False
