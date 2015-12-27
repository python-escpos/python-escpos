************
Dependencies
************

Fedora
------

Fortunately everything is on Fedora repositories.

::

    # yum install python-imaging pyserial pyusb python-qrcode

Ubuntu
------

Ultimately, this instructions also apply to Raspbian, in case you are
interested to install python-escpos on your Raspberry with Raspbian.

Install the packages available on distro repositories.

::

    # apt-get install python-imaging pyserial

The packages which are not available at Ubuntu repositories need to be
installed manually.

pyusb
^^^^^
This is the python binding to libusb-1.0 

* Get the latest tarball from `sourceforge <http://sourceforge.net/projects/pyusb/files/PyUSB%201.0/>`__
* Build and install it

::

    # tar zxvf pyusb-1.*.tar.gz
    # cd pyusb-1.*
    # python setup.py build
    # sudo python setup.py install

python-qrcode
^^^^^^^^^^^^^

This is the python module to generate QR Codes

* Checkout the latest code from `github <https://github.com/lincolnloop/python-qrcode>`__
* Build and install it

::

    # git clone https://github.com/lincolnloop/python-qrcode
    # cd python-qrcode
    # python setup.py build
    # sudo python setup.py install

