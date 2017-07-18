from escpos.printer import Usb


if __name__ == '__main__':

    # Adapt to your needs
    p = Usb(0x0416, 0x5011, profile="POS-5890")

    # Some software barcodes
    p.set(align='left')

    p.text("hello\n")

    p.qr("https://github.com/python-escpos/python-escpos")

    p.text("world\n")