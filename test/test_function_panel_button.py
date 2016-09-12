#!/usr/bin/python
"""tests for panel button function

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: GNU GPL v3
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from nose.tools import with_setup

import escpos.printer as printer
import os

devfile = 'testfile'


def setup_testfile():
    """create a testfile as devfile"""
    fhandle = open(devfile, 'a')
    try:
        os.utime(devfile, None)
    finally:
        fhandle.close()


def teardown_testfile():
    """destroy testfile again"""
    os.remove(devfile)


@with_setup(setup_testfile, teardown_testfile)
def test_function_panel_button_on():
    """test the panel button function (enabling) by comparing output"""
    instance = printer.File(devfile=devfile)
    instance.panel_buttons()
    instance.flush()
    with open(devfile, "rb") as f:
        assert(f.read() == b'\x1B\x63\x35\x00')


@with_setup(setup_testfile, teardown_testfile)
def test_function_panel_button_off():
    """test the panel button function (disabling) by comparing output"""
    instance = printer.File(devfile=devfile)
    instance.panel_buttons(False)
    instance.flush()
    with open(devfile, "rb") as f:
        assert(f.read() == b'\x1B\x63\x35\x01')
