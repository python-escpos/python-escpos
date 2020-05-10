#!/usr/bin/python
"""test the raising of errors with the error module

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2017 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import pytest
import escpos
import escpos.exceptions


def test_raise_error_wrongly():
    """raise error the wrong way

    should reproduce https://github.com/python-escpos/python-escpos/issues/257
    """
    with pytest.raises(AttributeError):
        raise escpos.Error("This should raise an AttributeError.")


def tests_raise_error():
    """raise error the right way"""
    with pytest.raises(escpos.exceptions.Error):
        raise escpos.exceptions.Error("This should raise an error.")
