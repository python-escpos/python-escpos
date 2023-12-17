#!/usr/bin/python
"""verifies that the metaclass abc is properly used by ESC/POS

:author: `Patrick Kanzler <dev@pkanzler.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 Patrick Kanzler
:license: MIT
"""

from abc import ABCMeta

import pytest

import escpos.escpos as escpos


def test_abstract_base_class_raises() -> None:
    """test whether the abstract base class raises an exception for ESC/POS"""
    with pytest.raises(TypeError):
        # This call should raise TypeError because of abstractmethod _raw()
        escpos.Escpos()  # type: ignore [abstract]


def test_abstract_base_class() -> None:
    """test whether Escpos has the metaclass ABCMeta"""
    assert issubclass(escpos.Escpos, object)
    assert type(escpos.Escpos) is ABCMeta
