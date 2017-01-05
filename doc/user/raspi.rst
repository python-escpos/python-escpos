************
Raspberry Pi
************

:Last Reviewed: 2017-01-05

This instructions were tested on Raspbian Jessie.

.. warning:: You should **never** directly connect an printer with RS232-interface (serial port) directly to
    a Raspberry PI or similar interface (e.g. those simple USB-sticks without encasing). Those interfaces are
    based on 5V- or 3,3V-logic (the latter in the case of Raspberry PI). Classical RS232 uses 12V-logic and would
    **thus destroy your interface**. Connect both systems with an appropriate *level shifter*.

Dependencies
------------
First, install the packages available on Raspbian.

::

       sudo apt-get install python3 python3-setuptools python3-pip libjpeg8-dev

Installation
------------
You can install by using pip3.

::

    sudo pip3 install --upgrade pip
    sudo pip3 install python-escpos

Run
---
You need sudo and python3 to run your program.

::

    sudo python3 your-program.py

Now you can attach your printer and and test it with the example code in the project's set of examples.
You can find that in the `project-repository <https://github.com/python-escpos/python-escpos>`__.

For more details on this check the :doc:`installation-manual <installation>`.
