ESCPOS
======

Python library to manipulate ESC/POS Printers.

Description
------------------------------------------------------------------

Python ESC/POS is a library which lets the user have access to all
those printers handled by ESC/POS commands, as defined by Epson,
from a Python application.

The standard usage is send raw text to the printer, but in also 
helps the user to enhance the experience with those printers by
facilitating the bar code printing in many different standards,
as well as manipulating images so they can be printed as brand
logo or any other usage images migh have. 

Text can be aligned/justified and fonts can be changed by size,
type and weight.

Also, this module handles some hardware functionalities like, cut
paper, carrier return, printer reset and others concerned to the
carriage alignment.


Dependencies
------------------------------------------------------------------

In order to start getting access to your printer, you must ensure
you have previously installed the following python modules:

  * pyusb (python-usb)
  * PIL (Python Image Library) or Pillow (recommended)


Feature List
------------------------------------------------------------------

  * Support for the following interfaces
    * USB
    * Serial
    * Network
    * File

  * Commands include
    * Text and image positioning
    * Text formatting
    * Opening cash drawers
    * Full/Partial cuts
    * Barcodes and QR Codes
    * Images and image scaling
    * Chinese character support

TODO
------------------------------------------------------------------

  * Testing
  * Possibly a virtual printer in the far future
  * Provide install instructions
  * Provide API documentation

USB Quickstart
------------------------------------------------------------------

### Find your printer ###

Before start create your Python ESC/POS printer instance, you must
see at your system for the printer parameters. On Linux this is done with
the 'lsusb' command.

First run the command to look for the "Vendor ID" and "Product ID",
then write down the values, these values are displayed just before
the name of the device with the following format:

    xxxx:xxxx

Example:
  Bus 002 Device 001: ID 1a2b:1a2b Device name

Write down the the values in question, then issue the following
command so you can get the "Interface" number and "End Point"

    lsusb -vvv -d xxxx:xxxx | grep iInterface
    lsusb -vvv -d xxxx:xxxx | grep bEndpointAddress | grep OUT

The first command will yields the "Interface" number that must
be handy to have and the second yields the "Output Endpoint"
address.

By default the "Interface" number is "0" and the "Output Endpoint"
address is "0x82",  if you have other values then you can define
with your instance.

### Define a printer instance and send commands ###

The following example shows how to initialize a printer over USB.

*** NOTE: Always finish the sequence with cut otherwise
          you will end up with weird chars being printed.

    from escpos import printer

    p = printer.Usb(0x04b8, 0x0202)
    p.text("Hello World")
    p.image("doge.jpg")
    p.fullimage("a.really.large.image.png")
    p.barcode('1324354657687','EAN13',64,2,'','')
    p.qr('this is a piece of code')
    p.cut()

Links
------------------------------------------------------------------

Project homepage originally at:

http://repo.bashlinux.com/projects/escpos.html

By Manuel F Martinez <manpaz@bashlinux.com>

Forked from https://code.google.com/p/python-escpos/
