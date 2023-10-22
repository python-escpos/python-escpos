#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the LP printer

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


def test_device_not_initialized(lpprinter):
    """
    GIVEN a lp printer object
    WHEN it is not initialized
    THEN check the device property is False
    """
    assert lpprinter._device is False


def test_open_raise_exception(lpprinter, devicenotfounderror, mocker):
    """
    GIVEN a lp printer object
    WHEN open() is set to raise a DeviceNotFoundError on error
    THEN check the exception is raised
    """
    mocker.patch("escpos.printer.LP.printers", new={"test_printer": "Test"})

    lpprinter.printer_name = "fakeprinter"

    with pytest.raises(devicenotfounderror):
        lpprinter.open(raise_not_found=True)


def test_open_not_raise_exception(lpprinter, caplog, mocker):
    """
    GIVEN a lp printer object
    WHEN open() is set to not raise on error but simply cancel
    THEN check the error is logged and open() canceled
    """
    mocker.patch("escpos.printer.LP.printers", new={"test_printer": "Test"})

    lpprinter.printer_name = "fakeprinter"

    with caplog.at_level(logging.ERROR):
        lpprinter.open(raise_not_found=False)

    assert "not available" in caplog.text
    assert lpprinter.device is None


def test_open(lpprinter, caplog, mocker):
    """
    GIVEN a lp printer object and a mocked connection
    WHEN a valid connection to a device is opened
    THEN check the success is logged and the device property is set
    """
    mocker.patch("subprocess.Popen")
    mocker.patch("escpos.printer.LP.printers", new={"test_printer": "Test"})

    lpprinter.printer_name = "test_printer"
    assert lpprinter.printer_name in lpprinter.printers

    with caplog.at_level(logging.INFO):
        lpprinter.open()

    assert "enabled" in caplog.text
    assert lpprinter.device


def test_close_on_reopen(lpprinter, mocker):
    """
    GIVEN a lp printer object and a mocked connection
    WHEN a valid connection to a device is reopened before close
    THEN check the close method is called if _device
    """
    spy = mocker.spy(lpprinter, "close")
    mocker.patch("subprocess.Popen")
    mocker.patch("escpos.printer.LP.printers", new={"test_printer": "Test"})

    lpprinter.printer_name = "test_printer"

    lpprinter.open()
    assert lpprinter._device

    lpprinter.open()
    spy.assert_called_once_with()


def test_flush(lpprinter, mocker):
    """
    GIVEN a lp printer object and a mocked connection
    WHEN auto_flush is disabled and flush() issued manually
    THEN check the flush method is called only one time.
    """
    spy = mocker.spy(lpprinter, "flush")
    mocker.patch("subprocess.Popen")
    mocker.patch("escpos.printer.LP.printers", new={"test_printer": "Test"})

    lpprinter.printer_name = "test_printer"
    lpprinter.auto_flush = False
    lpprinter.open()
    lpprinter.textln("python-escpos")
    lpprinter.flush()

    assert spy.call_count == 1


def test_auto_flush_on_command(lpprinter, mocker):
    """
    GIVEN a lp printer object and a mocked connection
    WHEN auto_flush is enabled and flush() not issued manually
    THEN check the flush method is called automatically
    """
    spy = mocker.spy(lpprinter, "flush")
    mocker.patch("subprocess.Popen")
    mocker.patch("escpos.printer.LP.printers", new={"test_printer": "Test"})

    lpprinter.printer_name = "test_printer"
    lpprinter.auto_flush = True
    lpprinter.open()
    lpprinter.textln("python-escpos")
    lpprinter.textln("test")

    assert spy.call_count > 1


def test_auto_flush_on_close(lpprinter, mocker, caplog, capsys):
    """
    GIVEN a lp printer object and a mocked connection
    WHEN auto_flush is disabled and flush() not issued manually
    THEN check the flush method is called automatically on close
    """
    spy = mocker.spy(lpprinter, "flush")
    mocker.patch("subprocess.Popen")
    mocker.patch("escpos.printer.LP.printers", new={"test_printer": "Test"})

    lpprinter.printer_name = "test_printer"
    lpprinter.auto_flush = False
    lpprinter.open()
    lpprinter.textln("python-escpos")
    lpprinter.close()

    assert spy.call_count == 1


def test_close(lpprinter, caplog, mocker):
    """
    GIVEN a lp printer object and a mocked connection
    WHEN a connection is opened and closed
    THEN check the closing is logged and the device property is False
    """
    mocker.patch("subprocess.Popen")
    mocker.patch("escpos.printer.LP.printers", new={"test_printer": "Test"})

    lpprinter.printer_name = "test_printer"
    lpprinter.open()

    with caplog.at_level(logging.INFO):
        lpprinter.close()

    assert "Closing" in caplog.text
    assert lpprinter._device is False
