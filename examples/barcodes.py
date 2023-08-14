"""Example for printing barcodes."""
from escpos.printer import Usb

# Adapt to your needs
p = Usb(0x0416, 0x5011, profile="TM-T88II")

# Print software and then hardware barcode with the same content
p.barcode("123456", "CODE39", width=2, force_software=True)
p.text("\n")
p.text("\n")
p.barcode("123456", "CODE39")
