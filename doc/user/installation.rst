************
Installation
************

System preparation
------------------

1. Install the required
   `dependencies <https://github.com/manpaz/python-escpos/wiki/Dependencies>`__

2. Get the *Product ID* and *Vendor ID* from the lsusb command
   ``# lsusb  Bus 002 Device 001: ID 1a2b:1a2b Device name``

3. Create a udev rule to let users belonging to *dialout* group use the
   printer. You can create the file
   ``/etc/udev/rules.d/99-escpos.rules`` and add the following:
   ``SUBSYSTEM=="usb", ATTRS{idVendor}=="1a2b", ATTRS{idProduct}=="1a2b", MODE="0664", GROUP="dialout"``
   Replace *idVendor* and *idProduct* hex numbers with the ones that you
   got from the previous step. Note that you can either, add yourself to
   "dialout" group, or use another group you already belongs instead
   "dialout" and set it in the ``GROUP`` parameter in the above rule.

4. Restart udev ``# sudo service udev restart`` In some new systems it
   is done with ``# sudo udevadm control --reload``

Install
-------

* Clone python-escpos from github
* Change directory to python-escpos and install the package

   ::

       # cd python-escpos
       # python setup.py build
       # sudo python setup.py install

* Enjoy !!!


