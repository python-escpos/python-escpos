#!/usr/bin/python
"""tests for the text printing function

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: GNU GPL v3
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
from hypothesis import given
import hypothesis.strategies as st

import escpos.printer as printer

@given(text=st.text())
def test_function_text_dies_ist_ein_test_lf(text):
    """test the text printing function with simple string and compare output"""
    instance = printer.Dummy()
    instance.magic.encode_text = mock.Mock()
    instance.text(text)
    instance.magic.encode_text.assert_called_with(txt=text)
