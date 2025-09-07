# /// script
# requires-python = ">=3.12"
# dependencies = ["python-escpos"]
# [tool.uv.sources]
# python-escpos = { path = "../", editable = true }
# ///
"""Example file for software barcodes."""
from escpos.printer import Usb


def main() -> None:
    """Main function."""
    p = Usb(0x0416, 0x5011, profile="POS-5890")

    # Some software barcodes
    p.barcode("Hello", "code128", width=2, force_software="bitImageRaster")
    p.barcode("1234", "code39", width=2, force_software=True)


if __name__ == "__main__":
    main()
