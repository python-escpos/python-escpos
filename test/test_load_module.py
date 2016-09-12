#!/usr/bin/python
"""very basic test cases that load the classes

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
def test_instantiation():
    """test the instantiation of a escpos-printer class and basic printing"""
    instance = printer.File(devfile=devfile)
    instance.text('This is a test\n')
