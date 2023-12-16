#!/usr/bin/python
"""basic test case that simulates an empty capability file

:author: `Patrick Kanzler <dev@pkanzler.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""

import os
import tempfile

import pytest


def test_instantiation() -> None:
    """test the instantiation of a escpos-printer class"""
    # inject an environment variable that points to an empty capabilities file
    os.environ["ESCPOS_CAPABILITIES_FILE"] = tempfile.NamedTemporaryFile().name

    import escpos.printer as printer
    from escpos.exceptions import BarcodeTypeError

    # remove again the variable (so that no other tests are affected)
    os.environ.pop("ESCPOS_CAPABILITIES_FILE")

    instance = printer.Dummy()
    with pytest.raises(BarcodeTypeError):
        instance.barcode("bc", "code")
