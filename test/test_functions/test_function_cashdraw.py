#!/usr/bin/python

import pytest

import escpos.printer as printer
from escpos.exceptions import CashDrawerError


def test_raise_CashDrawerError() -> None:
    """should raise an error if the sequence is invalid."""
    instance = printer.Dummy()
    with pytest.raises(CashDrawerError):
        # call with sequence that is too long
        instance.cashdraw([1, 1, 1, 1, 1, 1])
