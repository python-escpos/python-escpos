#!/usr/bin/python
"""tests for panel button function

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import escpos.printer as printer


def test_function_panel_button_on():
    """test the panel button function (enabling) by comparing output"""
    instance = printer.Dummy()
    instance.panel_buttons()
    assert instance.output == b"\x1B\x63\x35\x00"


def test_function_panel_button_off():
    """test the panel button function (disabling) by comparing output"""
    instance = printer.Dummy()
    instance.panel_buttons(False)
    assert instance.output == b"\x1B\x63\x35\x01"
