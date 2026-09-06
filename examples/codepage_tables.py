# /// script
# requires-python = ">=3.9"
# dependencies = ["python-escpos"]
# [tool.uv.sources]
# python-escpos = { path = "../", editable = true }
# ///
"""Prints code page tables."""

import sys

from escpos.constants import (
    CODEPAGE_CHANGE,
    CTL_CR,
    CTL_FF,
    CTL_HT,
    CTL_LF,
    CTL_VT,
    ESC,
)
from escpos.printer import Dummy


def print_codepage(printer: Dummy, codepage: str) -> None:
    """Print a code page."""
    if codepage.isdigit():
        printer._raw(CODEPAGE_CHANGE + bytes((int(codepage),)))
        printer._raw(b"after")
    else:
        printer.charcode(codepage)

    sep = ""

    # Table header
    printer.set(font="b")
    printer._raw(f"  {sep.join(map(lambda s: hex(s)[2:], range(0, 16)))}\n".encode())
    printer.set()

    # The table
    for x in range(0, 16):
        # First column
        printer.set(font="b")
        printer._raw(f"{hex(x)[2:]} ".encode())
        printer.set()

        for y in range(0, 16):
            byte = bytes(
                (x * 16 + y),
            )

            if byte in (ESC, CTL_LF, CTL_FF, CTL_CR, CTL_HT, CTL_VT):
                byte = b" "

            printer._raw(byte)
            printer._raw(sep.encode())
        printer._raw(b"\n")


def main() -> None:
    """Init printer and print codepage tables."""
    dummy = Dummy()

    dummy.hw("init")

    for codepage in sys.argv[1:] or ["USA"]:
        dummy.set(height=2, width=2)
        dummy._raw((codepage + "\n\n\n").encode())
        print_codepage(dummy, codepage)
        dummy._raw(b"\n\n")

    dummy.cut()

    print(dummy.output)


if __name__ == "__main__":
    main()
