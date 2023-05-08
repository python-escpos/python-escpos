#!/usr/bin/python
"""test the facility which enables usage of the with-statement

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import escpos.printer as printer
import escpos.escpos as escpos


def test_with_statement():
    """Use with statement"""
    dummy_printer = printer.Dummy()
    with escpos.EscposIO(dummy_printer) as p:
        p.writelines("Some text.\n")
    # TODO extend these tests as they don't really do anything at the moment
