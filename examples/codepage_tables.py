"""Prints code page tables.
"""


import six
import sys

from escpos import printer
from escpos.constants import (
    CODEPAGE_CHANGE,
    ESC,
    CTL_LF,
    CTL_FF,
    CTL_CR,
    CTL_HT,
    CTL_VT,
)


def main():
    dummy = printer.Dummy()

    dummy.hw("init")

    for codepage in sys.argv[1:] or ["USA"]:
        dummy.set(height=2, width=2)
        dummy._raw(codepage + "\n\n\n")
        print_codepage(dummy, codepage)
        dummy._raw("\n\n")

    dummy.cut()

    print(dummy.output)


def print_codepage(printer, codepage):
    if codepage.isdigit():
        codepage = int(codepage)
        printer._raw(CODEPAGE_CHANGE + six.int2byte(codepage))
        printer._raw("after")
    else:
        printer.charcode(codepage)

    sep = ""

    # Table header
    printer.set(font="b")
    printer._raw("  {}\n".format(sep.join(map(lambda s: hex(s)[2:], range(0, 16)))))
    printer.set()

    # The table
    for x in range(0, 16):
        # First column
        printer.set(font="b")
        printer._raw("{} ".format(hex(x)[2:]))
        printer.set()

        for y in range(0, 16):
            byte = six.int2byte(x * 16 + y)

            if byte in (ESC, CTL_LF, CTL_FF, CTL_CR, CTL_HT, CTL_VT):
                byte = " "

            printer._raw(byte)
            printer._raw(sep)
        printer._raw("\n")


if __name__ == "__main__":
    main()
