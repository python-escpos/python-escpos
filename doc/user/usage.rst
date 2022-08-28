*****
Usage
*****
:Last Reviewed: 2017-06-10

Define your printer
-------------------

USB printer
^^^^^^^^^^^

Before creating your Python ESC/POS printer instance, consult the system to obtain
the printer parameters. This is done with the 'lsusb' command.

Run the command and look for the "Vendor ID" and "Product ID" and write
down the values. These values are displayed just before the name
of the device with the following format:

::

    xxxx:xxxx

Example:

::

    # lsusb
    Bus 002 Device 001: ID 04b8:0202 Epson ...

Write down the the values in question, then issue the following command
so you can get the "Interface" number and "End Point"

::

    # lsusb -vvv -d xxxx:xxxx | grep iInterface
        iInterface              0
    # lsusb -vvv -d xxxx:xxxx | grep bEndpointAddress | grep OUT
          bEndpointAddress     0x01  EP 1 OUT

The first command will yield the "Interface" number that must be handy
to have and the second yields the "Output Endpoint" address.

**USB Printer initialization**

::

    p = printer.Usb(0x04b8,0x0202)

By default the "Interface" number is "0" and the "Output Endpoint"
address is "0x01". If you have other values then you can define them on
your instance. So, assuming that we have another printer, CT-S2000,
manufactured by Citizen (with "Vendor ID" of 2730 and "Product ID" of 0fff)
where in\_ep is on 0x81 and out\_ep=0x02, then the printer definition should
look like:

**Generic USB Printer initialization**

::

    p = printer.Usb(0x2730, 0x0fff, 0, 0x81, 0x02)

Network printer
^^^^^^^^^^^^^^^

You only need the IP of your printer, either because it is getting its
IP by DHCP or you set it manually.

**Network Printer initialization**

::

    p = printer.Network("192.168.1.99")

Serial printer
^^^^^^^^^^^^^^

Most of the default values set by the DIP switches for the serial
printers, have been set as default on the serial printer class, so the
only thing you need to know is which serial port the printer is connected
to.

**Serial printer initialization**

::

    p = printer.Serial("/dev/tty0")

    # on a Windows OS serial devices are typically accessible as COM
    p = printer.Serial("COM1")

Other printers
^^^^^^^^^^^^^^

Some printers under `/dev` can't be used or initialized with any of the
methods described above. Usually, those are printers used by printcap,
however, if you know the device name, you could try to initialize by
passing the device node name.

::

    p = printer.File("/dev/usb/lp1")

The default is "/dev/usb/lp0", so if the printer is located on that
node, then you don't necessary need to pass the node name.

Define your instance
--------------------

The following example demonstrates how to initialize the Epson TM-TI88IV
on a USB interface.

::

    from escpos import *
    """ Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
    p = printer.Usb(0x04b8,0x0202)
    # Print text
    p.text("Hello World\n")
    # Print image
    p.image("logo.gif")
    # Print QR Code
    p.qr("You can readme from your smartphone")
    # Print barcode
    p.barcode('1324354657687','EAN13',64,2,'','')
    # Cut paper
    p.cut()

Standard python constraints on libraries apply. This means especially
that you should not name the script in which you implement these lines
should not be named ``escpos`` as this would collide with the name of
the library.

Configuration File
------------------

You can create a configuration file for python-escpos. This will
allow you to use the CLI, and skip some setup when using the library
programmatically.

The default configuration file is named ``config.yaml`` and uses the YAML
format. For windows it is probably at::

    %appdata%/python-escpos/config.yaml

And for linux::

    $HOME/.config/python-escpos/config.yaml

If you aren't sure, run::

    from escpos import config
    c = config.Config()
    c.load()

If it can't find the configuration file in the default location, it will tell
you where it's looking. You can always pass a path, or a list of paths, to
the ``load()`` method.

To load the configured printer, run::

    from escpos import config
    c = config.Config()
    printer = c.printer()


The printer section
^^^^^^^^^^^^^^^^^^^

The ``printer`` configuration section defines a default printer to create.

The only required parameter is ``type``. The value of this has to be one of the
printers defined in :doc:`/user/printers`.

The rest of the given parameters will be passed on to the initialization of the printer class.
Use these to overwrite the default values as specified in :doc:`/user/printers`.
This implies that the parameters have to match the parameter-names of the respective printer class.

An example file printer::

    printer:
            type: File
            devfile: /dev/someprinter

And for a network printer::

    printer:
            type: Network
            host: 127.0.0.1
            port: 9000

An USB-printer could be defined by::

    printer:
            type: Usb
            idVendor: 0x1234
            idProduct: 0x5678
            in_ep: 0x66
            out_ep: 0x01

Printing text right
-------------------

Python-escpos is designed to accept unicode.

For normal usage you can simply pass your text to the printers ``text()``-function. It will automatically guess
the right codepage and then send the encoded data to the printer. If this feature does not work, please try to
isolate the error and then create an issue on the GitHub project page.

If you want or need to you can manually set the codepage. For this please use the ``charcode()``-function. You can set
any key-value that is in ``CHARCODE``. If something is wrong, an ``CharCodeError`` will be raised.
After you have manually set the codepage the printer won't change it anymore. You can revert to normal behaviour
by setting charcode to ``AUTO``.

Advanced Usage: Print from binary blob
--------------------------------------

Imagine you have a file with ESC/POS-commands in binary form. This could be useful for testing capabilities of your
printer with a known working combination of commands.
You can print this data with the following code, using the standard methods of python-escpos. (This is an
advantage of the fact that `_raw()` accepts binary strings.)

::

    from escpos import printer
    p = printer.Serial()  # adapt this to your printer model

    file = open("binary-blob.bin", "rb")  # read in the file containing your commands in binary-mode
    data = file.read()
    file.close()

    p._raw(data)

That's all, the printer should then print your data. You can also use this technique to let others reproduce an issue
that you have found. (Just "print" your commands to a File-printer on your local filesystem.)
However, please keep in mind, that often it is easier and better to just supply the code that you are using.

Here you can download an example, that will print a set of common barcodes:

    * :download:`barcode.bin </download/barcode.bin>` by `@mike42 <https://github.com/mike42>`_

Advanced Usage: change capabilities-profile
-------------------------------------------

Packaged together with the escpos-code is a capabilities-file. This file in
JSON-format describes the capabilities of different printers. It is developed and hosted in
`escpos-printer-db <https://github.com/receipt-print-hq/escpos-printer-db>`_.

Certain applications like the usage of `cx_freeze <https://cx-freeze.readthedocs.io>`_ might change the
packaging structure. This leads to the capabilities-profile not being found.
In this case you can use the environment-variable `ESCPOS_CAPABILITIES_FILE`.
The following code is an example.

.. code-block:: shell

   # use packaged capabilities-profile
   python-escpos cut

   # use capabilities-profile that you have put in /usr/python-escpos
   export ESCPOS_CAPABILITIES_FILE=/usr/python-escpos/capabilities.json
   python-escpos cut

   # use packaged file again
   unset ESCPOS_CAPABILITIES_FILE
   python-escpos cut


Hint: preprocess printing
-------------------------

Printing images directly to the printer is rather slow.
One factor that slows down the process is the transmission over e.g. serial port.

Apart from configuring your printer to use the maximum baudrate (in the case of serial-printers), there is not much
that you can do.
However you could use the :py:class:`escpos.printer.Dummy`-printer to preprocess your image.
This is probably best explained by an example:

.. code-block:: Python

   from escpos.printer import Serial, Dummy

   p = Serial()
   d = Dummy()

   # create ESC/POS for the print job, this should go really fast
   d.text("This is my image:\n")
   d.image("funny_cat.png")
   d.cut()

   # send code to printer
   p._raw(d.output)

This way you could also store the code in a file and print it later.
You could then for example print the code from another process than your main-program and thus reduce the waiting time.
(Of course this will not make the printer print faster.)

Troubleshooting
---------------

This section gathers various hints on troubleshooting.

Print with STAR TSP100 family
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Printer of the STAR TSP100 family do not have a native ESC/POS mode, which
is why you will not be able to directly print with this library to the printer.

More information on this topic can be found in the online documentation of
`Star Micronics <https://www.starmicronics.com/help-center/knowledge-base/configure-tsp100-series-printers-esc-pos-mode/>`_
and the `discussion in the python-escpos project <https://github.com/python-escpos/python-escpos/issues/410>`_.


