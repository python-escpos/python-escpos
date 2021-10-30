from escpos.printer import Usb


# Adapt to your needs
p = Usb(0x0416, 0x5011, profile="POS-5890")

# Print software and then hardware barcode with the same content
p.soft_barcode("code39", "123456")
p.text("\n")
p.text("\n")
p.barcode("123456", "CODE39")
