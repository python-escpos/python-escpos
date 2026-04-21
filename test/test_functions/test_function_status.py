#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for status queries

:author: Benito López and the python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2026 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""

import logging

import pytest

from escpos.constants import RT_STATUS_ONLINE, RT_STATUS_PAPER
from escpos.exceptions import ValidationError


@pytest.mark.parametrize("resp", [b"\x12", b"\x7e"])
# valid bytes: '0b00010010', '0b01111110'
def test_check_valid_response(driver, resp) -> None:
    """
    GIVEN a dummy printer object
    WHEN valid bytes are passed to the response checker
    THEN check the checks are passed
    """
    assert driver._check_valid_response(resp) is True


@pytest.mark.parametrize("resp", [b"", b"\x10\x04", b"\x81\x01\x80\x02\x10"])
# invalid bytes: empty, multiple, 0b10000001, 0b00000001, 0b10000000, 0b00000010, 0b00010000
def test_check_invalid_response(driver, resp) -> None:
    """
    GIVEN a dummy printer object
    WHEN invalid bytes are passed to the response checker
    THEN check the checks are not passed
    """
    assert driver._check_valid_response(resp) is False


def test_query_status_error(driver, mocker, caplog) -> None:
    """
    GIVEN a dummy printer object
    WHEN non valid response is read
    THEN raise ValidationError, log error and check return value
    """
    mocker.patch("escpos.printer.Dummy._read", return_value=b"")
    with pytest.raises(ValidationError):
        driver.query_status(RT_STATUS_PAPER, raise_not_valid=True)

    with caplog.at_level(logging.ERROR):
        status = driver.query_status(RT_STATUS_ONLINE, raise_not_valid=False)

    assert "Invalid status data" in caplog.text
    assert status == b""


def test_query_is_online_error(driver, mocker, caplog) -> None:
    """
    GIVEN a dummy printer object
    WHEN non valid response is read
    THEN log error and check return value
    """
    mocker.patch("escpos.printer.Dummy._read", return_value=b"")
    with caplog.at_level(logging.WARNING):
        status = driver.is_online()

    assert "Unknown online status data" in caplog.text
    assert status is False


def test_query_is_online(driver, mocker) -> None:
    """
    GIVEN a dummy printer object
    WHEN a valid response is read
    THEN check return value
    """
    mocker.patch("escpos.printer.Dummy._read", return_value=b"\x12")
    status = driver.is_online()

    assert status is True


def test_paper_status_error(driver, mocker, caplog) -> None:
    """
    GIVEN a dummy printer object
    WHEN non valid response is read
    THEN log error and check return value
    """
    mocker.patch("escpos.printer.Dummy._read", return_value=b"")
    with caplog.at_level(logging.WARNING):
        status = driver.paper_status()

    assert "Unknown paper status data" in caplog.text
    assert status == 0


@pytest.mark.parametrize("resp, expected", [(b"\x12", 2), (b"\x1e", 1)])
def test_query_paper_status(driver, mocker, resp, expected) -> None:
    """
    GIVEN a dummy printer object
    WHEN a valid response is read
    THEN check return value is the expected
    """
    mocker.patch("escpos.printer.Dummy._read", return_value=resp)
    status = driver.paper_status()

    assert status == expected
