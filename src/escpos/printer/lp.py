#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the CupsPrinter printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""

import os
import subprocess
import sys

from ..escpos import Escpos

if not sys.platform.startswith("win"):

    class LP(Escpos):
        """Simple UNIX lp command raw printing.

        Thanks to `Oyami-Srk comment <https://github.com/python-escpos/python-escpos/pull/348#issuecomment-549558316>`_.

        inheritance:

        .. inheritance-diagram:: escpos.printer.LP
            :parts: 1

        """

        def __init__(self, printer_name: str, *args, **kwargs):
            """LP class constructor.

            :param printer_name: CUPS printer name (Optional)
            :type printer_name: str
            :param auto_flush: Automatic flush after every _raw() (Optional)
            :type auto_flush: bool
            """
            Escpos.__init__(self, *args, **kwargs)
            self.printer_name = printer_name
            self.auto_flush = kwargs.get("auto_flush", True)
            self.open()

        def open(self):
            """Invoke _lp_ in a new subprocess and wait for commands."""
            self.lp = subprocess.Popen(
                ["lp", "-d", self.printer_name, "-o", "raw"],
                stdin=subprocess.PIPE,
                stdout=open(os.devnull, "w"),
            )

        def close(self):
            """Stop the subprocess."""
            self.lp.terminate()

        def flush(self):
            """End line and wait for new commands."""
            if self.lp.stdin.writable():
                self.lp.stdin.write(b"\n")
            if self.lp.stdin.closed is False:
                self.lp.stdin.close()
            self.lp.wait()
            self.open()

        def _raw(self, msg):
            """Write raw command(s) to the printer.

            :param msg: arbitrary code to be printed
            :type msg: bytes
            """
            if self.lp.stdin.writable():
                self.lp.stdin.write(msg)
            else:
                raise Exception("Not a valid pipe for lp process")
            if self.auto_flush:
                self.flush()
