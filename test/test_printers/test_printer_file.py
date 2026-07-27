#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the File printer

:author: `Patrick Kanzler <dev@pkanzler.de>`_ and the python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016-2023 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""

import logging

import pytest


def test_device_not_initialized(fileprinter):
    """
    GIVEN a file printer object
    WHEN it is not initialized
    THEN check the device property is False
    """
    assert fileprinter._device is False


def test_open_raise_exception(fileprinter, devicenotfounderror):
    """
    GIVEN a file printer object
    WHEN open() is set to raise a DeviceNotFoundError on error
    THEN check the exception is raised
    """
    fileprinter.devfile = "fake/device"

    with pytest.raises(devicenotfounderror):
        fileprinter.open(raise_not_found=True)


def test_open_not_raise_exception(fileprinter, caplog):
    """
    GIVEN a file printer object
    WHEN open() is set to not raise on error but simply cancel
    THEN check the error is logged and open() canceled
    """
    fileprinter.devfile = "fake/device"

    with caplog.at_level(logging.ERROR):
        fileprinter.open(raise_not_found=False)

    assert "not found" in caplog.text
    assert fileprinter.device is None


def test_open(fileprinter, caplog, temp_path):
    """
    GIVEN a file printer object bound to an existing file
    WHEN a valid connection to a device is opened
    THEN check the success is logged and the device property is set
    """
    tmpfile = temp_path / "test_open.bin"
    tmpfile.touch()
    fileprinter.devfile = tmpfile
    with caplog.at_level(logging.INFO):
        fileprinter.open()

    assert "enabled" in caplog.text
    assert fileprinter.device


def test_close_on_reopen(fileprinter, mocker, temp_path):
    """
    GIVEN a file printer object bound to an existing file
    WHEN a valid connection to a device is reopened before close
    THEN check the close method is called if _device
    """
    spy = mocker.spy(fileprinter, "close")

    tmpfile = temp_path / "test_close_on_reopen.bin"
    tmpfile.touch()
    fileprinter.devfile = tmpfile
    fileprinter.open()
    assert fileprinter._device

    fileprinter.open()
    spy.assert_called_once_with()


def test_flush(fileprinter, mocker, temp_path):
    """
    GIVEN a file printer object bound to an existing file
    WHEN auto_flush is disabled and flush() issued manually
    THEN check the flush method is called only one time.
    """
    spy = mocker.spy(fileprinter, "flush")

    tmpfile = temp_path / "test_flush.bin"
    tmpfile.touch()
    fileprinter.devfile = tmpfile
    fileprinter.auto_flush = False
    fileprinter.open()
    fileprinter.textln("python-escpos")
    fileprinter.flush()

    assert spy.call_count == 1


def test_auto_flush_on_command(fileprinter, mocker, temp_path):
    """
    GIVEN a file printer object bound to an existing file
    WHEN auto_flush is enabled and flush() not issued manually
    THEN check the flush method is called automatically
    """
    spy = mocker.spy(fileprinter, "flush")

    tmpfile = temp_path / "test_auto_flush_on_command.bin"
    tmpfile.touch()
    fileprinter.devfile = tmpfile
    fileprinter.auto_flush = True
    fileprinter.open()
    fileprinter.textln("python-escpos")
    fileprinter.textln("test")

    assert spy.call_count > 1


def test_auto_flush_on_close(fileprinter, mocker, temp_path):
    """
    GIVEN a file printer object bound to an existing file
    WHEN auto_flush is disabled and flush() not issued manually
    THEN check the flush method is called automatically on close
    """
    spy = mocker.spy(fileprinter, "flush")

    tmpfile = temp_path / "test_autoflush_on_close.bin"
    tmpfile.touch()
    fileprinter.devfile = tmpfile
    fileprinter.auto_flush = False
    fileprinter.open()
    fileprinter.textln("python-escpos")
    fileprinter.close()

    assert spy.call_count == 1


def test_read(fileprinter, caplog, temp_path):
    """
    GIVEN a file printer object bound to an existing file
    WHEN reading the file buffer even with auto_flush disabled
    THEN check a warning is logged for auto_flush and the last byte is read and response is correct.
    """
    tmpfile = temp_path / "test_read.bin"
    tmpfile.touch()
    fileprinter.devfile = tmpfile
    fileprinter.open()
    fileprinter._raw(b"\x08\x12")
    fileprinter.auto_flush = False

    with caplog.at_level(logging.WARNING):
        resp = fileprinter._read()

    assert "Param 'auto_flush' is disabled" in caplog.text
    assert resp == b"\x12"


def test_close(fileprinter, caplog, temp_path):
    """
    GIVEN a file printer object bound to an existing file
    WHEN a connection is opened and closed
    THEN check the closing is logged and the device property is False
    """
    tmpfile = temp_path / "test_close.bin"
    tmpfile.touch()
    fileprinter.devfile = tmpfile
    fileprinter.open()

    with caplog.at_level(logging.INFO):
        fileprinter.close()

    assert "Closing" in caplog.text
    assert fileprinter._device is False
