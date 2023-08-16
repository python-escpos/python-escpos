#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the CupsPrinter printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""

from ..escpos import Escpos


def is_usable() -> bool:
    """Indicate whether this component can be used due to dependencies."""
    return True


class Dummy(Escpos):
    """Dummy printer.

    This class is used for saving commands to a variable, for use in situations where
    there is no need to send commands to an actual printer. This includes
    generating print jobs for later use, or testing output.

    inheritance:

    .. inheritance-diagram:: escpos.printer.Dummy
        :parts: 1

    """

    @staticmethod
    def is_usable() -> bool:
        """Indicate whether this printer class is usable.

        Will return True if dependencies are available.
        Will return False if not.
        """
        return is_usable()

    def __init__(self, *args, **kwargs):
        """Init with empty output list."""
        Escpos.__init__(self, *args, **kwargs)
        self._output_list = []

    def _raw(self, msg):
        """Print any command sent in raw format.

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        self._output_list.append(msg)

    @property
    def output(self):
        """Get the data that was sent to this printer."""
        return b"".join(self._output_list)

    def clear(self):
        """Clear the buffer of the printer.

        This method can be called if you send the contents to a physical printer
        and want to use the Dummy printer for new output.
        """
        del self._output_list[:]

    def close(self):
        """Close not implemented for Dummy printer."""
        pass
