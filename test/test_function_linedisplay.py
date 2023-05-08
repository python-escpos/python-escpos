#!/usr/bin/python
"""tests for line display

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2017 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import escpos.printer as printer


def test_function_linedisplay_select_on():
    """test the linedisplay_select function (activate)"""
    instance = printer.Dummy()
    instance.linedisplay_select(select_display=True)
    assert instance.output == b"\x1B\x3D\x02"


def test_function_linedisplay_select_off():
    """test the linedisplay_select function (deactivate)"""
    instance = printer.Dummy()
    instance.linedisplay_select(select_display=False)
    assert instance.output == b"\x1B\x3D\x01"


def test_function_linedisplay_clear():
    """test the linedisplay_clear function"""
    instance = printer.Dummy()
    instance.linedisplay_clear()
    assert instance.output == b"\x1B\x40"
