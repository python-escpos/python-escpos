Printers
========

:Last Reviewed: 2023-08-23

As of now there are 8 different types of printer implementations.

USB
---
The USB-class uses pyusb and libusb to communicate with USB-based
printers.

.. note::
      This driver is not suited for USB-to-Serial-adapters
      and similar devices, but only for those implementing native USB.

.. autoclass:: escpos.printer.Usb
    :members:
    :special-members:
    :member-order: bysource
    :noindex:

Serial
------
This driver uses pyserial in order to communicate with serial devices.
If you are using an USB-based adapter to connect to the serial port,
then you should also use this driver.
The configuration is often based on DIP-switches that you can set on your
printer. For the hardware-configuration please refer to your printer's manual.

.. autoclass:: escpos.printer.Serial
     :members:
     :special-members:
     :member-order: bysource
     :noindex:

Network
-------

This driver is based on the socket class.

.. autoclass:: escpos.printer.Network
      :members:
      :special-members:
      :member-order: bysource
      :noindex:

Troubleshooting
^^^^^^^^^^^^^^^
Problems with a network-attached printer can have numerous causes.
Make sure that your device has a proper IP address.
Often you can check the IP address by triggering the self-test of the device.
As a next step try to send text manually to the device.
You could use for example:

    ::

            echo "OK\n" | nc IPADDRESS 9100
            # the port number is often 9100

As a last resort try to reset the interface of the printer.
This should be described in its manual.

File
----
This printer "prints" just into a file-handle.
Especially on \*nix-systems this comes very handy.

.. autoclass:: escpos.printer.File
      :members:
      :special-members:
      :member-order: bysource
      :noindex:

Dummy
-----
The Dummy-printer is mainly for testing- and debugging-purposes.
It stores all of the "output" as raw ESC/POS in a string and returns that.

.. autoclass:: escpos.printer.Dummy
      :members:
      :member-order: bysource
      :noindex:

CUPS
----
This driver uses `pycups` in order to communicate with a CUPS server.
Supports both local and remote CUPS printers and servers.
The printer must be properly configured in CUPS administration.
The connector generates a print job that is added to the CUPS queue.

.. autoclass:: escpos.printer.CupsPrinter
      :members:
      :member-order: bysource
      :noindex:

LP
----
This driver uses the UNIX command `lp` in order to communicate with a CUPS server.
Supports local and remote CUPS printers.
The printer must be properly configured in CUPS administration.
The connector spawns a new sub-process where the command lp is executed.

No dependencies required, but somehow the print queue will affect some
print job such as barcode.

.. autoclass:: escpos.printer.LP
      :members:
      :special-members:
      :member-order: bysource
      :noindex:

Win32Raw
--------
This driver uses a native WIN32 interface of Windows in order to print.
Please refer to the code for documentation as this driver is currently
not included in the documentation build.

.. autoclass:: escpos.printer.Win32Raw
      :members:
      :special-members:
      :member-order: bysource
      :noindex: