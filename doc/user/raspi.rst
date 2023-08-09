Raspberry Pi
============

:Last Reviewed: 2023-08-10

.. warning:: You should **never** directly connect an printer with RS232-interface
    (serial port) directly to a Raspberry PI or similar interface
    (e.g. those simple USB-sticks without encasing).
    Those interfaces are based on 5V- or 3,3V-logic
    (the latter in the case of Raspberry PI).
    Classical RS232 uses 12V-logic and would **thus destroy your interface**.
    Connect both systems with an appropriate *level shifter*.

Installation
------------
The installation should be performed as described in :ref:`user_installation`.

Run
---
You can run this software as on any other Linux system.

Attach your printer and test it with the example code in the project's set of examples.
You can find that in the
`project-repository <https://github.com/python-escpos/python-escpos>`__.

For more details on this check the :doc:`installation-manual <installation>`.
