"""Example file for software barcodes."""
from escpos.printer import Usb

# Adapt to your needs
p = Usb(0x0416, 0x5011, profile="POS-5890")

# Some software barcodes
p.barcode("Hello", "code128", width=2, force_software="bitImageRaster")
p.barcode("1234", "code39", width=2, force_software=True)
