.. _user_installation:

Installation
============

:Last Reviewed: 2023-08-10

Installation with PIP
---------------------
Installation should be rather straight-forward. python-escpos is on PyPi,
so you can simply enter:

    ::

        pip install python-escpos[all]

This should install all necessary dependencies. Apart from that
python-escpos is for some versions also available as a Debian package.
If you want to always benefit from the newest stable releases you should
always install from PyPi.
If you use the ``--pre`` parameter for ``pip``, you will get the latest
pre-release.

The following installation options exist:

 * `all`: install all packages available for this platform
 * `usb`: install packages required for USB printers
 * `serial`: install packages required for serial printers
 * `win32`: install packages required for win32 printing (only Windows)
 * `cups`: install packages required for CUPS printing

Other installation methods
--------------------------
Officially, no other installation methods are supplied.

If you want to install nevertheless from another source,
please make sure that you have received the correct package
and that the capabilities data is properly integrated.
When packaging from source please read the developer
information in :ref:`developer-manual-repository`.

If your packaging method breaks the resource system from setuptools,
it might be necessary to supply the path to the capabilities file:
:ref:`advanced-usage-change-capabilities-profile`.

Setup udev for USB-Printers
---------------------------
1. Get the *Product ID* and *Vendor ID* from the lsusb command
   ``# lsusb  Bus 002 Device 001: ID 1a2b:1a2b Device name``.
   (Or whichever way your system supplies to get the PID and VID.)

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
python-escpos has a CLI with tab-completion.
This is realized with ``argcomplete``.
In order for this to work you have to enable tab-completion, which is described in
the `manual of argcomplete <https://argcomplete.readthedocs.io>`__.

If you only want to enable it for python-escpos, or global activation does not work, try this:

    ::

        eval "$(register-python-argcomplete python-escpos)"


