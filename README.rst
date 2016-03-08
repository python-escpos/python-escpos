#############################################################
python-escpos - Python library to manipulate ESC/POS Printers
#############################################################

.. image:: https://travis-ci.org/python-escpos/python-escpos.svg?branch=master
    :target: https://travis-ci.org/python-escpos/python-escpos
    :alt: Continous Integration

.. image:: https://www.quantifiedcode.com/api/v1/project/95748b89a3974700800b85e4ed3d32c4/badge.svg
    :target: https://www.quantifiedcode.com/app/project/95748b89a3974700800b85e4ed3d32c4
    :alt: Code issues

.. image:: https://landscape.io/github/python-escpos/python-escpos/master/landscape.svg?style=flat
    :target: https://landscape.io/github/python-escpos/python-escpos/master
    :alt: Code Health

.. image:: https://readthedocs.org/projects/python-escpos/badge/?version=stable
    :target: http://python-escpos.readthedocs.org/en/latest/?badge=stable
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

Dependencies
------------

This library makes use of:

    * pyusb for USB-printers
    * Pillow for image printing
    * qrcode for the generation of QR-codes
    * pyserial for serial printers

Documentation and Usage
-----------------------

The basic usage is:

.. code:: python

    from escpos import *

    """ Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
    Epson = escpos.Escpos(0x04b8,0x0202,0)
    Epson.text("Hello World")
    Epson.image("logo.gif")
    Epson.barcode('1324354657687','EAN13',64,2,'','')
    Epson.cut()

The full project-documentation is available on `Read the Docs <https://python-escpos.readthedocs.org>`_.

Contributing
------------

This project is open for any contribution!