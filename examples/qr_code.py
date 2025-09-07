# /// script
# requires-python = ">=3.12"
# dependencies = ["python-escpos"]
# [tool.uv.sources]
# python-escpos = { path = "../", editable = true }
# ///
"""Print example QR codes."""
import sys

from escpos.printer import Usb


def main() -> None:
    """Main function."""
    if len(sys.argv) != 2:
        print("usage: qr_code.py <content>")
        sys.exit(1)

    content = sys.argv[1]

    # Adapt to your needs
    p = Usb(0x0416, 0x5011, profile="POS-5890")
    p.qr(content, center=True)

if __name__ == "__main__":
    main()
