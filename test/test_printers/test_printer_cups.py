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


def test_device_not_initialized(cupsprinter) -> None:
    """
    GIVEN a cups printer object
    WHEN it is not initialized
    THEN check the device property is False
    """
    assert cupsprinter._device is False


def test_open_raise_exception(cupsprinter, devicenotfounderror) -> None:
    """
    GIVEN a cups printer object
    WHEN open() is set to raise a DeviceNotFoundError on error
    THEN check the exception is raised
    """
    cupsprinter.host = "fakehost"

    with pytest.raises(devicenotfounderror):
        cupsprinter.open(raise_not_found=True)


def test_open_not_raise_exception(cupsprinter, caplog) -> None:
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


def test_open(cupsprinter, caplog, mocker) -> None:
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


def test_close_on_reopen(cupsprinter, mocker) -> None:
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
    spy.assert_called_once()


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


def test_send_on_close(cupsprinter, mocker) -> None:
    """
    GIVEN a cups printer object and a mocked pycups device
    WHEN closing connection before send the buffer
    THEN check the buffer is sent and cleared
    """
    mocked_cups = mocker.patch("cups.Connection")

    spy_send = mocker.spy(cupsprinter, "send")
    spy_clear = mocker.spy(cupsprinter, "_clear")

    cupsprinter._device = mocked_cups
    cupsprinter.pending_job = True

    cupsprinter.close()

    spy_send.assert_called_once()
    spy_clear.assert_called_once()
    assert cupsprinter.pending_job is False


def test_raw_raise_exception(cupsprinter) -> None:
    """
    GIVEN a cups printer object
    WHEN passing a non byte string to _raw()
    THEN check an exception is raised and pending_job is False
    """
    with pytest.raises(TypeError):
        cupsprinter._raw("Non bytes")

    assert cupsprinter.pending_job is False


def test_raw(cupsprinter) -> None:
    """
    GIVEN a cups printer object
    WHEN passing a byte string to _raw()
    THEN check the buffer content
    """
    cupsprinter._raw(b"Test")
    cupsprinter.tmpfile.seek(0)
    assert cupsprinter.tmpfile.read() == b"Test"


def test_printers_no_device(cupsprinter) -> None:
    """
    GIVEN a cups printer object
    WHEN device is None
    THEN check the return value is {}
    """
    cupsprinter.device = None
    assert cupsprinter.printers == {}


def test_read_no_device(cupsprinter) -> None:
    """
    GIVEN a cups printer object
    WHEN device is None
    THEN check the return value is b'8'
    """
    cupsprinter.device = None
    assert cupsprinter._read() == b"8"
