#!/usr/bin/python
"""test the raising of errors with the error module

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2017 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import escpos


def test_raise_error():
    """raise error

    should reproduce https://github.com/python-escpos/python-escpos/issues/257
    """
    raise escpos.Error("This is a test.")
