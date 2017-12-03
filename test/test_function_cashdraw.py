#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import escpos.printer as printer
from escpos.exceptions import CashDrawerError
import pytest


def test_raise_CashDrawerError():
    """should raise an error if the sequence is invalid.
    """
    instance = printer.Dummy()
    with pytest.raises(CashDrawerError):
        # call with sequence that is too long
        instance.cashdraw([1,1,1,1,1,1])

