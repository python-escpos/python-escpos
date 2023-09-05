Printing Barcodes
-----------------

:Last Reviewed: 2023-08-10

Many printers implement barcode printing natively.
These hardware rendered barcodes are fast but the supported
formats are limited by the printer itself and different between models.
However, almost all printers support printing images, so barcode
rendering can be performed externally by software and then sent
to the printer as an image.
As a drawback, this operation is much slower and the user needs
to know and choose the image implementation method supported by
the printer's command-set.

barcode-method
~~~~~~~~~~~~~~
Since version 3.0, the ``barcode`` method unifies the previous
``barcode`` (hardware) and ``soft_barcode`` (software) methods.
It is able to choose automatically the best printer implementation
for barcode printing based on the capabilities of the printer
and the type of barcode desired.
To achieve this, it relies on the information contained in the
escpos-printer-db profiles.
The chosen profile needs to match the capabilities of the printer
as closely as possible.

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

A very good description on CODE128 is also on
`Wikipedia <https://en.wikipedia.org/wiki/Code_128>`_.
