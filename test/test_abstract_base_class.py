#!/usr/bin/python
"""verifies that the metaclass abc is properly used by ESC/POS

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 Patrick Kanzler
:license: MIT
"""


from nose.tools import raises

import escpos.escpos as escpos
from abc import ABCMeta


@raises(TypeError)
def test_abstract_base_class_raises():
    """test whether the abstract base class raises an exception for ESC/POS"""
    escpos.Escpos()  # This call should raise TypeError because of abstractmethod _raw()


def test_abstract_base_class():
    """test whether Escpos has the metaclass ABCMeta"""
    assert issubclass(escpos.Escpos, object)
    assert type(escpos.Escpos) is ABCMeta
