************
Raspberry Pi
************

:Last Reviewed: 2016-12-07

This instructions were tested on Raspbian.

.. warning:: You should **never** directly connect an printer with RS232-interface (serial port) directly to
    a Raspberry PI or similar interface (e.g. those simple USB-sticks without encasing). Those interfaces are
    based on 5V- or 3,3V-logic (the latter in the case of Raspberry PI). Classical RS232 uses 12V-logic and would
    **thus destroy your interface**. Connect both systems with an appropriate *level shifter*.

Normal installation
-------------------
Normally you should be able to install the library just like on any other
Linux distribution. Please be reminded that the newer versions are not in Debian
and thus not in Raspbian.
However, you can just install with `pip`. For more details on this
check the :doc:`installation-manual <installation>`.

If this works for you, you don't need to continue reading this part.
If not, please check if the rest might help you.
Should you have any problems, do not hesitate to contact the maintainer, since you
might have found a bug in the code or documentation.

Dependencies
------------

First, install the packages available on Raspbian.

::

    apt-get install python-imaging python-serial python-setuptools

PyUSB
^^^^^

.. todo:: The freshness of this part is not verified. Please take it with a grain of salt or help updating it.

PyUSB 1.0 is not available on Ubuntu, so you have to download and
install it manually.

1. Download the latest tarball from
   `Sourceforge <http://sourceforge.net/projects/pyusb/files/>`__
2. Decompress the zip file
3. Install the library

   ::

       # wget ...
       unzip pyusb*.zip
       cd pyusb*
       python setup.py build
       sudo python setup.py install

python-qrcode
^^^^^^^^^^^^^

You can install qrcode just from pip with

   ::

      sudo pip install qrcode

Otherwise you can install it manually. If in doubt please check the documentation of the
`python-qrcode`-project.

1. Checkout the code from github
2. Install the library

   ::

       git clone https://github.com/lincolnloop/python-qrcode
       cd python-qrcode
       python setup.py build
       sudo python setup.py install

Installation
------------

If you have installed pyusb for libusb-1.0 then you need to:

1. Download the latest file
2. Decompress the file
3. Install the library

::

    git clone --recursive https://github.com/python-escpos/python-escpos.git
    cd python-escpos
    python setup.py build
    sudo python setup.py install

Now you can attach your printer and and test it with the example code in
the project's set of examples. You can find that in the `project-repository <https://github.com/python-escpos/python-escpos>`__.
