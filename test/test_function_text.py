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

import pytest
import mock
from hypothesis import given, assume
import hypothesis.strategies as st
from escpos.printer import Dummy


def get_printer():
    return Dummy(magic_encode_args={'disabled': True, 'encoding': 'cp437'})


@given(text=st.text())
def test_text(text):
    """Test that text() calls the MagicEncode object.
    """
    instance = get_printer()
    instance.magic.write = mock.Mock()
    instance.text(text)
    instance.magic.write.assert_called_with(text)


def test_block_text():
    printer = get_printer()
    printer.block_text(
        "All the presidents men were eating falafel for breakfast.", font='a')
    assert printer.output == \
        b'All the presidents men were eating falafel\nfor breakfast.'
