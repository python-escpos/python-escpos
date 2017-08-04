#############################################################
python-escpos - Python library to manipulate ESC/POS Printers
#############################################################

.. image:: https://travis-ci.org/python-escpos/python-escpos.svg?branch=master
    :target: https://travis-ci.org/python-escpos/python-escpos
    :alt: Continous Integration

.. image:: https://landscape.io/github/python-escpos/python-escpos/master/landscape.svg?style=flat
    :target: https://landscape.io/github/python-escpos/python-escpos/master
    :alt: Code Health

.. image:: https://codecov.io/github/python-escpos/python-escpos/coverage.svg?branch=master
    :target: https://codecov.io/github/python-escpos/python-escpos?branch=master
    :alt: Code Coverage

.. image:: https://readthedocs.org/projects/python-escpos/badge/?version=stable
    :target: http://python-escpos.readthedocs.io/en/latest/?badge=stable
    :alt: Documentation Status


Description
-----------

Python ESC/POS is a library which lets the user have access to all those printers handled
by ESC/POS commands, as defined by Epson, from a Python application.

The library tries to implement the functions provided by the ESC/POS-commandset and supports sending text, images,
barcodes and qr-codes to the printer.

Text can be aligned/justified and fonts can be changed by size, type and weight.

Also, this module handles some hardware functionalities like cutting paper, control characters, printer reset
and similar functions.

Since supported commands differ from printer to printer the software tries to automatically apply the right
settings for the printer that you set. These settings are handled by
`escpos-printer-db <https://github.com/receipt-print-hq/escpos-printer-db>`_ which is also used in
`escpos-php <https://github.com/mike42/escpos-php>`_.

Dependencies
------------

This library makes use of:

* `pyusb <https://github.com/walac/pyusb>`_ for USB-printers
* `Pillow <https://github.com/python-pillow/Pillow>`_ for image printing
* `qrcode <https://github.com/lincolnloop/python-qrcode>`_ for the generation of QR-codes
* `pyserial <https://github.com/pyserial/pyserial>`_ for serial printers
* `viivakoodi <https://github.com/kxepal/viivakoodi>`_ for the generation of barcodes

Documentation and Usage
-----------------------

The basic usage is:

.. code:: python

    from escpos.printer import Usb

    """ Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
    p = Usb(0x04b8, 0x0202, 0, profile="TM-T88III")
    p.text("Hello World\n")
    p.image("logo.gif")
    p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
    p.cut()

The full project-documentation is available on `Read the Docs <https://python-escpos.readthedocs.io>`_.

Contributing
------------

This project is open for any contribution! Please see CONTRIBUTING.rst for more information.
