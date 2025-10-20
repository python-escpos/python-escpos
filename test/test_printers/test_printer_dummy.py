#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the Dummy printer

:author: Benito López and the python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2025 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


def test_clear(driver) -> None:
    """
    GIVEN a dummy printer object
    WHEN clear method is called
    THEN check the return value is the expected
    """
    driver.text("Hello")
    driver.clear()
    assert driver.output == b""


def test_read_no_output(driver) -> None:
    """
    GIVEN a dummy printer object with no output data
    WHEN reading the last byte of data 
    THEN check the return value is the expected
    """
    driver.clear()
    assert driver._read() == b""


def test_read(driver) -> None:
    """
    GIVEN a dummy printer object
    WHEN reading the last byte of data
    THEN check the return value is the expected
    """
    driver._raw(b"\x10\x04\x01")  # RT_STATUS_ONLINE
    assert driver._read() == b"\x01"
    driver._raw(b"\x12")  # Simulate an 'is online' response
    assert driver._read() == b"\x12"
