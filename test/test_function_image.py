#!/usr/bin/python
"""tests for the image printing function

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
def test_function_image_with_50x50_png():
    """test the image function with 50x50.png (grayscale png)"""
    instance = printer.File(devfile=devfile)
    instance.image("test/50x50.png")

@with_setup(setup_testfile, teardown_testfile)
def test_function_image_with_255x255_png():
    """test the image function with 255x255.png (grayscale png)"""
    instance = printer.File(devfile=devfile)
    instance.image("test/255x255.png")

@with_setup(setup_testfile, teardown_testfile)
def test_function_image_with_400x400_png():
    """test the image function with 400x400.png (grayscale png)"""
    instance = printer.File(devfile=devfile)
    instance.image("test/400x400.png")
