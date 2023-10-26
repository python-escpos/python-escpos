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


def test_device_not_initialized(win32rawprinter):
    """
    GIVEN a win32raw printer object
    WHEN it is not initialized
    THEN check the device property is False
    """
    assert win32rawprinter._device is False


def test_open_raise_exception(win32rawprinter, devicenotfounderror):
    """
    GIVEN a win32raw printer object
    WHEN open() is set to raise a DeviceNotFoundError on error
    THEN check the exception is raised
    """
    win32rawprinter.printer_name = "fake_printer"

    with pytest.raises(devicenotfounderror):
        win32rawprinter.open(raise_not_found=True)


def test_open_not_raise_exception(win32rawprinter, caplog):
    """
    GIVEN a win32raw printer object
    WHEN open() is set to not raise on error but simply cancel
    THEN check the error is logged and open() canceled
    """
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
    # The _win32typing.PyPrinterHANDLE object is unreachable, so we have to mock it
    PyPrinterHANDLE = mocker.Mock()
    PyPrinterHANDLE.return_value = 0  # Accepts 0 or None as return value

    # Replace the contents of Win32Raw.printers to accept test_printer as a system's printer name
    mocker.patch("escpos.printer.Win32Raw.printers", new={"test_printer": "Test"})

    # Configure and assert printer_name is valid
    win32rawprinter.printer_name = "test_printer"
    assert win32rawprinter.printer_name in win32rawprinter.printers

    with caplog.at_level(logging.INFO):
        # Patch the win32print.OpenPrinter method to return the mocked PyPrinterHANDLE
        mocker.patch("win32print.OpenPrinter", new=PyPrinterHANDLE)
        win32rawprinter.open()

    assert "enabled" in caplog.text
    assert win32rawprinter.device == PyPrinterHANDLE.return_value


def test_close_on_reopen(win32rawprinter, mocker):
    """
    GIVEN a win32raw printer object and a mocked win32print device
    WHEN a valid connection to a device is reopened before close
    THEN check the close method is called if _device
    """
    # The _win32typing.PyPrinterHANDLE object is unreachable, so we have to mock it
    PyPrinterHANDLE = mocker.Mock()
    PyPrinterHANDLE.return_value = 0  # Accepts 0 or None as return value

    # Replace the contents of Win32Raw.printers to accept test_printer as a system's printer name
    mocker.patch("escpos.printer.Win32Raw.printers", new={"test_printer": "Test"})

    # Configure printer_name
    win32rawprinter.printer_name = "test_printer"

    # Patch the win32print.OpenPrinter method to return the mocked PyPrinterHANDLE
    mocker.patch("win32print.OpenPrinter", new=PyPrinterHANDLE)
    # Patch the win32print close methods
    mocker.patch("win32print.EndPagePrinter")
    mocker.patch("win32print.EndDocPrinter")
    mocker.patch("win32print.ClosePrinter")

    spy = mocker.spy(win32rawprinter, "close")
    # Simulate a reopen before close
    win32rawprinter._device = True
    win32rawprinter.open()

    spy.assert_called_once()


def test_close(win32rawprinter, caplog, mocker):
    """
    GIVEN a win32raw printer object and a mocked win32print device
    WHEN a connection is opened and closed
    THEN check the closing is logged and the device property is False
    """
    # The _win32typing.PyPrinterHANDLE object is unreachable, so we have to mock it
    PyPrinterHANDLE = mocker.Mock()
    PyPrinterHANDLE.return_value = 0  # Accepts 0 or None as return value

    # Replace the contents of Win32Raw.printers to accept test_printer as a system's printer name
    mocker.patch("escpos.printer.Win32Raw.printers", new={"test_printer": "Test"})

    # Configure and assert printer_name is valid
    win32rawprinter.printer_name = "test_printer"
    assert win32rawprinter.printer_name in win32rawprinter.printers

    # Patch the win32print.OpenPrinter method to return the mocked PyPrinterHANDLE
    mocker.patch("win32print.OpenPrinter", new=PyPrinterHANDLE)
    win32rawprinter.open()
    with caplog.at_level(logging.INFO):
        # Patch the win32print close methods
        # Raises a warning but passes the test
        mocker.patch("win32print.EndPagePrinter")
        mocker.patch("win32print.EndDocPrinter")
        mocker.patch("win32print.ClosePrinter")
        win32rawprinter.close()

    assert "Closing" in caplog.text
    assert win32rawprinter._device is False


def test_raw_raise_exception(win32rawprinter, devicenotfounderror):
    """
    GIVEN a win32raw printer object and a mocked win32print device
    WHEN calling _raw() before configuring the connection
    THEN check an exception is raised
    """
    win32rawprinter.printer_name = None
    with pytest.raises(devicenotfounderror):
        win32rawprinter._raw(b"Test error")

    win32rawprinter.printer_name = "fake_printer"
    win32rawprinter.device = None
    with pytest.raises(devicenotfounderror):
        win32rawprinter._raw(b"Test error")


def test_raw(win32rawprinter, mocker):
    """
    GIVEN a win32raw printer object and a mocked win32print device
    WHEN calling _raw() after a valid connection
    THEN check the underlying method is correctly called
    """
    PyPrinterHANDLE = mocker.Mock()
    PyPrinterHANDLE.return_value = 0

    mocked_writer = mocker.patch("win32print.WritePrinter")

    win32rawprinter._device = PyPrinterHANDLE
    win32rawprinter._raw(b"Test error")

    mocked_writer.assert_called_once_with(PyPrinterHANDLE, b"Test error")
