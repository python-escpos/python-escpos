****
TODO
****

Introduction
------------

python-escpos is the initial idea, from here we can start to build a
robust library to get most of the ESC/POS printers working with this
library.

Eventually, this library must be able to cover almost all the defined
models detailed in the ESC/POS Command Specification Manual.

Details
-------

What things are planned to work on?

Testing
~~~~~~~

* Test on many printers as possible (USB, Serial, Network)
* automate testing

Design
~~~~~~

* Add all those sequences which are not common, but part of the ESC/POS
  Command Specifications.

  *  Port to Python 3
  *  Windows compatibility (hidapi instead libusb?)
  *  PDF417 support

* use something similar to the `capabilities` in escpos-php

Todos in the codebase
~~~~~~~~~~~~~~~~~~~~~

.. todolist::


