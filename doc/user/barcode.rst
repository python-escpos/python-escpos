Printing Barcodes
-----------------
:Last Reviewed: 2016-07-31

Most ESC/POS-printers implement barcode-printing.
The barcode-commandset is implemented in the barcode-method.
For a list of compatible barcodes you should check the manual of your printer.
As a rule of thumb: even older Epson-models support most 1D-barcodes.
To be sure just try some implementations and have a look at the notices below.

barcode-method
~~~~~~~~~~~~~~
The barcode-method is rather low-level and orients itself on the implementation of ESC/POS.
In the future this class could be supplemented by a high-level class that helps the user generating the payload.

.. py:currentmodule:: escpos.escpos

.. automethod:: Escpos.barcode
    :noindex:

CODE128
~~~~~~~
Code128 barcodes need a certain format.
For now the user has to make sure that the payload is correct.
For alphanumeric CODE128 you have to preface your payload with `{B`.

.. code-block:: Python

   from escpos.printer import Dummy, Serial
   p = Serial()
   # print CODE128 012ABCDabcd
   p.barcode("{B012ABCDabcd", "CODE128", function_type="B")

A very good description on CODE128 is also on `Wikipedia <https://en.wikipedia.org/wiki/Code_128>`_.
