************
Installation
************

:Last Reviewed: 2016-07-23

Installation with PIP
---------------------
Installation should be rather straight-forward. python-escpos is on PyPi, so you can simply enter:

    ::

        pip install python-escpos

This should install all necessary dependencies. Apart from that python-escpos should also be
available as a Debian package. If you want to always benefit from the newest stable releases you should probably
install from PyPi.

Setup udev for USB-Printers
---------------------------
1. Get the *Product ID* and *Vendor ID* from the lsusb command
   ``# lsusb  Bus 002 Device 001: ID 1a2b:1a2b Device name``

2. Create a udev rule to let users belonging to *dialout* group use the
   printer. You can create the file
   ``/etc/udev/rules.d/99-escpos.rules`` and add the following:
   ``SUBSYSTEM=="usb", ATTRS{idVendor}=="1a2b", ATTRS{idProduct}=="1a2b", MODE="0664", GROUP="dialout"``
   Replace *idVendor* and *idProduct* hex numbers with the ones that you
   got from the previous step. Note that you can either, add yourself to
   "dialout" group, or use another group you already belongs instead
   "dialout" and set it in the ``GROUP`` parameter in the above rule.

3. Restart udev ``# sudo service udev restart`` In some new systems it
   is done with ``# sudo udevadm control --reload``

Enabling tab-completion in CLI
------------------------------
python-escpos has a CLI with tab-completion. This is realised with ``argcomplete``.
In order for this to work you have to enable tab-completion, which is described in
the `manual of argcomplete <https://argcomplete.readthedocs.io>`__.

If you only want to enable it for python-escpos, or global activation does not work, try this:

    ::

        eval "$(register-python-argcomplete python-escpos)"


