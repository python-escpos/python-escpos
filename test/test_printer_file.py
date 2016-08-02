#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the File printer

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: GNU GPL v3
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six

import mock
from hypothesis import given
from hypothesis.strategies import text

import escpos.printer as printer

if six.PY3:
    mock_open_call = 'builtins.open'
else:
    mock_open_call = '__builtin__.open'

@given(path=text())
@mock.patch(mock_open_call)
@mock.patch('escpos.escpos.Escpos.__init__')
def test_load_file_printer(mock_escpos, mock_open, path):
    """test the loading of the file-printer"""
    printer.File(devfile=path)
    assert mock_escpos.called
    mock_open.assert_called_with(path, "wb")


@given(txt=text())
@mock.patch.object(printer.File, 'device')
@mock.patch(mock_open_call)
@mock.patch('escpos.escpos.Escpos.__init__')
def test_auto_flush(mock_escpos, mock_open, mock_device, txt):
    """test auto_flush in file-printer"""
    p = printer.File(auto_flush=False)
    # inject the mocked device-object
    p.device = mock_device
    p._raw(txt)
    assert not mock_device.flush.called
    mock_device.reset_mock()
    p = printer.File(auto_flush=True)
    # inject the mocked device-object
    p.device = mock_device
    p._raw(txt)
    assert mock_device.flush.called


@given(txt=text())
@mock.patch.object(printer.File, 'device')
@mock.patch(mock_open_call)
def test_flush_on_close(mock_open, mock_device, txt):
    """test flush on close in file-printer"""
    p = printer.File(auto_flush=False)
    # inject the mocked device-object
    p.device = mock_device
    p._raw(txt)
    assert not mock_device.flush.called
    p.close()
    assert mock_device.flush.called
    assert mock_device.close.called
