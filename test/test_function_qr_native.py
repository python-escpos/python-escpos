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
from escpos.constants import QR_ECLEVEL_H, QR_MODEL_1

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
def test_function_qr_defaults():
    """test QR code with defaults"""
    instance = printer.File(devfile=devfile)
    instance.qr("1234", native=True)
    instance.flush()
    with open(devfile, "rb") as f:
        assert(f.read() == b'\x1d(k\x04\x001A2\x00\x1d(k\x03\x001C\x03\x1d(k\x03\x001E0\x1d(k\x07\x001P01234\x1d(k\x03\x001Q0')

@with_setup(setup_testfile, teardown_testfile)
def test_function_qr_empty():
    """test QR printing blank code"""
    instance = printer.File(devfile=devfile)
    instance.qr("", native=True)
    instance.flush()
    with open(devfile, "rb") as f:
        assert(f.read() == b'')

@with_setup(setup_testfile, teardown_testfile)
def test_function_qr_ec():
    """test QR error correction setting"""
    instance = printer.File(devfile=devfile)
    instance.qr("1234", native=True, ec=QR_ECLEVEL_H)
    instance.flush()
    with open(devfile, "rb") as f:
        assert(f.read() == b'\x1d(k\x04\x001A2\x00\x1d(k\x03\x001C\x03\x1d(k\x03\x001E3\x1d(k\x07\x001P01234\x1d(k\x03\x001Q0')

@with_setup(setup_testfile, teardown_testfile)
def test_function_qr_size():
    """test QR box size"""
    instance = printer.File(devfile=devfile)
    instance.qr("1234", native=True, size=7)
    instance.flush()
    with open(devfile, "rb") as f:
        assert(f.read() == b'\x1d(k\x04\x001A2\x00\x1d(k\x03\x001C\x07\x1d(k\x03\x001E0\x1d(k\x07\x001P01234\x1d(k\x03\x001Q0')

@with_setup(setup_testfile, teardown_testfile)
def test_function_qr_model():
    """test QR model"""
    instance = printer.File(devfile=devfile)
    instance.qr("1234", native=True, model=QR_MODEL_1)
    instance.flush()
    with open(devfile, "rb") as f:
        assert(f.read() == b'\x1d(k\x04\x001A1\x00\x1d(k\x03\x001C\x03\x1d(k\x03\x001E0\x1d(k\x07\x001P01234\x1d(k\x03\x001Q0')