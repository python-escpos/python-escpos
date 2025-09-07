# /// script
# requires-python = ">=3.12"
# dependencies = ["python-escpos"]
# [tool.uv.sources]
# python-escpos = { path = "../", editable = true }
# ///
"""Example for printing barcodes."""
from escpos.printer import Usb


def main() -> None:
    """Main function."""
    p = Usb(0x0416, 0x5011, profile="TM-T88II")

    # Print software and then hardware barcode with the same content
    p.barcode("123456", "CODE39", width=2, force_software=True)
    p.text("\n")
    p.text("\n")
    p.barcode("123456", "CODE39")


if __name__ == "__main__":
    main()
