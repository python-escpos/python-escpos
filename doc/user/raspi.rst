************
Raspberry Pi
************

This instructions were tested on Raspbian.

Unless you have done any distro with libusb-1.0 on the Raspberry Pi, the
following instructions should works fine on your raspberry distro.

.. warning:: You should **never** directly connect an printer with RS232-interface (serial port) directly to
    a Raspberry PI or similar interface (e.g. those simple USB-sticks without encasing). Those interfaces are
    based on 5V- or 3,3V-logic (the latter in the case of Raspberry PI). Classical RS232 uses 12V-logic and would
    **thus destroy your interface**. Connect both systems with an appropriate *level shifter*.

Dependencies
------------

First, install the packages available on Raspbian.

::

    # apt-get install python-imaging python-serial python-setuptools

PyUSB
^^^^^

PyUSB 1.0 is not available on Ubuntu, so you have to download and
install it manually

1. Download the latest tarball from
   `Sourceforge <http://sourceforge.net/projects/pyusb/files/>`__
2. Decompress the zip file
3. Install the library

   ::

       # wget ...
       # unzip pyusb*.zip
       # cd pyusb*
       # python setup.py build
       # sudo python setup.py install

python-qrcode
^^^^^^^^^^^^^

1. Checkout the code from github
2. Install the library

   ::

       # git clone https://github.com/lincolnloop/python-qrcode
       # cd python-qrcode
       # python setup.py build
       # sudo python setup.py install

Installation
------------

If you have installed pyusb for libusb-1.0 then you need to:

1. Download the latest file
2. Decompress the file
3. Install the library

::

    # git clone https://github.com/manpaz/python-escpos.git
    # cd python-escpos
    # python setup.py build
    # sudo python setup.py install

Now you can attach your printer and and test it with the example code in
the project's `home <https://github.com/manpaz/python-escpos>`__
