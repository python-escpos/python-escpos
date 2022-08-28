#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the File printer

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import six

import pytest
from hypothesis import given, settings
from hypothesis.strategies import text

import escpos.printer as printer

if six.PY3:
    mock_open_call = "builtins.open"
else:
    mock_open_call = "__builtin__.open"


@pytest.mark.skip("this test is broken and has to be fixed or discarded")
@given(path=text())
def test_load_file_printer(mocker, path):
    """test the loading of the file-printer"""
    mock_escpos = mocker.patch("escpos.escpos.Escpos.__init__")
    mock_open = mocker.patch(mock_open_call)
    printer.File(devfile=path)
    assert mock_escpos.called
    mock_open.assert_called_with(path, "wb")


@pytest.mark.skip("this test is broken and has to be fixed or discarded")
@given(txt=text())
def test_auto_flush(mocker, txt):
    """test auto_flush in file-printer"""
    mock_escpos = mocker.patch("escpos.escpos.Escpos.__init__")
    mock_open = mocker.patch(mock_open_call)
    mock_device = mocker.patch.object(printer.File, "device")

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


@pytest.mark.skip("this test is broken and has to be fixed or discarded")
@given(txt=text())
def test_flush_on_close(mocker, txt):
    """test flush on close in file-printer"""
    mock_open = mocker.patch(mock_open_call)
    mock_device = mocker.patch.object(printer.File, "device")

    p = printer.File(auto_flush=False)
    # inject the mocked device-object
    p.device = mock_device
    p._raw(txt)
    assert not mock_device.flush.called
    p.close()
    assert mock_device.flush.called
    assert mock_device.close.called
