.. python-escpos documentation master file, created by
   sphinx-quickstart on Sat Dec 26 14:28:42 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to python-escpos's documentation!
=========================================

Python ESC/POS is a library which lets the user have access to all those printers handled by ESC/POS commands, as defined by Epson, from a Python application.

The standard usage is send raw text to the printer, but in also helps the user to enhance the experience with those printers by facilitating the bar code printing in many different standards,as well as manipulating images so they can be printed as brand logo or any other usage images migh have.

Text can be justified and fonts can be changed by size, type and weight.

Also, this module handles some hardware functionalists like, cut paper, cash drawer kicking, printer reset, carriage return and others concerned to the carriage alignment.

------------

There are some different printers I'd like to acquire, unfortunately
not all, even used, are cheaper and easy to get.

If you want to help funding money to get more printers or just want to
donate because you like the project, please be in touch and I'll be
sending my PayPal info so you can donate.

Thank you!

User Documentation
------------------

.. toctree::
   :maxdepth: 1

   user/dependencies
   user/installation
   user/methods
   user/printers
   user/raspi
   user/todo
   user/usage

API
---

.. toctree::
   :maxdepth: 1
   
   api/escpos
   api/printer
   api/constants
   api/exceptions

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

