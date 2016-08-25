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

from nose.tools import with_setup

import escpos.printer as printer
from escpos.printer import Dummy
import os

import filecmp

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
def test_function_text_dies_ist_ein_test_lf():
    """test the text printing function with simple string and compare output"""
    instance = printer.File(devfile=devfile)
    instance.text('Dies ist ein Test.\n')
    instance.flush()
    assert(filecmp.cmp('test/Dies ist ein Test.LF.txt', devfile))


def test_block_text():
    printer = Dummy()
    printer.block_text(
        "All the presidents men were eating falafel for breakfast.", font='a')
    assert printer.output == \
        'All the presidents men were eating falafel\nfor breakfast.'
