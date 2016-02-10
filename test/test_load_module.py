#!/usr/bin/python
"""very basic test cases that load the classes

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_ and others
:organization: Bashlinux and `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: GNU GPL v3
"""

from nose.tools import with_setup

import escpos.printer as printer
import os

def setup_testfile():
    """create a testfile as devfile"""
    fhandle = open('testfile', 'a')
    try:
        os.utime('testfile', None)
    finally:
        fhandle.close()

def teardown_testfile():
    """destroy testfile again"""
    os.remove('testfile')

@with_setup(setup_testfile, teardown_testfile)
def test_instantiation():
    """test the instantiation of a escpos-printer class and basic printing"""
    instance = printer.File(devfile='testfile')
    instance.text('This is a test\n')
