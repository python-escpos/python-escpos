#!/usr/bin/python
"""very basic test cases that load the classes

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import escpos.printer as printer


def test_instantiation():
    """test the instantiation of a escpos-printer class and basic printing"""
    instance = printer.Dummy()
    instance.text('This is a test\n')
