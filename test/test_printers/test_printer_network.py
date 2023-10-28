#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the Network printer

:author: `Patrick Kanzler <dev@pkanzler.de>`_ and the python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016-2023 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""

import logging

import pytest


def test_device_not_initialized(networkprinter):
    """
    GIVEN a network printer object
    WHEN it is not initialized
    THEN check the device property is False
    """
    assert networkprinter._device is False


def test_open_raise_exception(networkprinter, devicenotfounderror):
    """
    GIVEN a network printer object
    WHEN open() is set to raise a DeviceNotFoundError on error
    THEN check the exception is raised
    """
    networkprinter.host = "fakehost"

    with pytest.raises(devicenotfounderror):
        networkprinter.open(raise_not_found=True)


def test_open_not_raise_exception(networkprinter, caplog):
    """
    GIVEN a network printer object
    WHEN open() is set to not raise on error but simply cancel
    THEN check the error is logged and open() canceled
    """
    networkprinter.host = "fakehost"

    with caplog.at_level(logging.ERROR):
        networkprinter.open(raise_not_found=False)

    assert "not found" in caplog.text
    assert networkprinter.device is None


def test_open(networkprinter, caplog, mocker):
    """
    GIVEN a network printer object and a mocked socket device
    WHEN a valid connection to a device is opened
    THEN check the success is logged and the device property is set
    """
    mocker.patch("socket.socket")

    with caplog.at_level(logging.INFO):
        networkprinter.open()

    assert "enabled" in caplog.text
    assert networkprinter.device


def test_close_on_reopen(networkprinter, mocker):
    """
    GIVEN a network printer object and a mocked connection
    WHEN a valid connection to a device is reopened before close
    THEN check the close method is called if _device
    """
    mocker.patch("socket.socket")
    spy = mocker.spy(networkprinter, "close")

    networkprinter.open()
    assert networkprinter._device

    networkprinter.open()
    spy.assert_called_once_with()


def test_close(networkprinter, caplog, mocker):
    """
    GIVEN a network printer object and a mocked socket device
    WHEN a connection is opened and closed
    THEN check the closing is logged and the device property is False
    """
    mocker.patch("socket.socket")
    networkprinter.open()

    with caplog.at_level(logging.INFO):
        networkprinter.close()

    assert "Closing" in caplog.text
    assert networkprinter._device is False
