from escpos.printer import Usb


# Adapt to your needs
p = Usb(0x0416, 0x5011, profile="POS-5890")

# Some software barcodes
p.soft_barcode("code128", "Hello")
p.soft_barcode("code39", "1234")
