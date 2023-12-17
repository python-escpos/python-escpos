#!/usr/bin/python
"""test the facility which enables usage of the with-statement

:author: `Patrick Kanzler <dev@pkanzler.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import escpos.escpos as escpos
import escpos.printer as printer


def test_with_statement() -> None:
    """Use with statement

    .. todo:: Extend these tests as they don't really do anything at the moment"""
    dummy_printer = printer.Dummy()
    with escpos.EscposIO(dummy_printer) as p:
        p.writelines("Some text.\n")
