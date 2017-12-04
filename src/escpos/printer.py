#!/usr/bin/python
#  -*- coding: utf-8 -*-
""" This module contains the implementations of abstract base class :py:class:`Escpos`.

:author: `Manuel F Martinez <manpaz@bashlinux.com>`_ and others
:organization: Bashlinux and `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2017 Bashlinux and python-escpos
:license: MIT
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from usb1 import USBContext

import platform
import serial
import socket

from .escpos import Escpos
from .exceptions import USBNotFoundError


class Usb(Escpos):
    """ USB printer

    This class describes a printer that natively speaks USB.

    inheritance:

    .. inheritance-diagram:: escpos.printer.Usb
        :parts: 1

    """
    INTERFACE = 0

    def __init__(self, idVendor, idProduct, timeout=0, in_ep=0x82, out_ep=0x01, *args, **kwargs):  # noqa: N803
        """
        :param idVendor: Vendor ID
        :param idProduct: Product ID
        :param timeout: Is the time limit of the USB operation. Default without timeout.
        :param in_ep: Input end point
        :param out_ep: Output end point
        """
        Escpos.__init__(self, *args, **kwargs)
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.timeout = timeout
        self.in_ep = in_ep
        self.out_ep = out_ep
        self.open()

    def open(self):
        """ Search device on USB tree and set it as escpos device """
        self.ctx = USBContext()
        dev = self.ctx.getByVendorIDAndProductID(self.idVendor, self.idProduct)
        if dev is None:
            raise USBNotFoundError("Device not found or cable not plugged in.")

        self.device = dev.open()
        if platform.system() == 'Linux' and self.device.kernelDriverActive(self.INTERFACE):
            self.device.detachKernelDriver(self.INTERFACE)

        self.device.claimInterface(self.INTERFACE)

    def _raw(self, msg):
        """ Print any command sent in raw format

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        self.device.bulkWrite(self.out_ep, msg, timeout=self.timeout)

    def _read(self):
        """ Reads a data buffer and returns it to the caller. """
        return self.device.bulkRead(self.in_ep, 16, timeout=self.timeout)

    def close(self):
        """ Release USB interface """
        if self.device:
            self.device.releaseInterface(self.INTERFACE)
            self.device.close()
            self.device = None
        if self.ctx:
            self.ctx.exit()
            self.ctx = None


class Serial(Escpos):
    """ Serial printer

    This class describes a printer that is connected by serial interface.

    inheritance:

    .. inheritance-diagram:: escpos.printer.Serial
        :parts: 1

    """

    def __init__(self, devfile="/dev/ttyS0", baudrate=9600, bytesize=8, timeout=1,
                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                 xonxoff=False, dsrdtr=True, *args, **kwargs):
        """

        :param devfile:  Device file under dev filesystem
        :param baudrate: Baud rate for serial transmission
        :param bytesize: Serial buffer size
        :param timeout:  Read/Write timeout
        :param parity:   Parity checking
        :param stopbits: Number of stop bits
        :param xonxoff:  Software flow control
        :param dsrdtr:   Hardware flow control (False to enable RTS/CTS)
        """
        Escpos.__init__(self, *args, **kwargs)
        self.devfile = devfile
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.dsrdtr = dsrdtr

        self.open()

    def open(self):
        """ Setup serial port and set is as escpos device """
        if self.device is not None and self.device.is_open:
            self.close()
        self.device = serial.Serial(port=self.devfile, baudrate=self.baudrate,
                                    bytesize=self.bytesize, parity=self.parity,
                                    stopbits=self.stopbits, timeout=self.timeout,
                                    xonxoff=self.xonxoff, dsrdtr=self.dsrdtr)

        if self.device is not None:
            print("Serial printer enabled")
        else:
            print("Unable to open serial printer on: {0}".format(str(self.devfile)))

    def _raw(self, msg):
        """ Print any command sent in raw format

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        self.device.write(msg)

    def _read(self):
        """ Reads a data buffer and returns it to the caller. """
        return self.device.read(16)

    def close(self):
        """ Close Serial interface """
        if self.device is not None and self.device.is_open:
            self.device.flush()
            self.device.close()


class Network(Escpos):
    """ Network printer

    This class is used to attach to a networked printer. You can also use this in order to attach to a printer that
    is forwarded with ``socat``.

    If you have a local printer on parallel port ``/dev/usb/lp0`` then you could start ``socat`` with:

    .. code-block:: none

        socat -u TCP4-LISTEN:4242,reuseaddr,fork OPEN:/dev/usb/lp0

    Then you should be able to attach to port ``4242`` with this class.
    Otherwise the normal usecase would be to have a printer with ethernet interface. This type of printer should
    work the same with this class. For the address of the printer check its manuals.

    inheritance:

    .. inheritance-diagram:: escpos.printer.Network
        :parts: 1

    """

    def __init__(self, host, port=9100, timeout=60, *args, **kwargs):
        """

        :param host:    Printer's hostname or IP address
        :param port:    Port to write to
        :param timeout: timeout in seconds for the socket-library
        """
        Escpos.__init__(self, *args, **kwargs)
        self.host = host
        self.port = port
        self.timeout = timeout
        self.open()

    def open(self):
        """ Open TCP socket with ``socket``-library and set it as escpos device """
        self.device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device.settimeout(self.timeout)
        self.device.connect((self.host, self.port))

        if self.device is None:
            print("Could not open socket for {0}".format(self.host))

    def _raw(self, msg):
        """ Print any command sent in raw format

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        self.device.sendall(msg)

    def close(self):
        """ Close TCP connection """
        if self.device is not None:
            self.device.shutdown(socket.SHUT_RDWR)
            self.device.close()


class File(Escpos):
    """ Generic file printer

    This class is used for parallel port printer or other printers that are directly attached to the filesystem.
    Note that you should stay away from using USB-to-Parallel-Adapter since they are unreliable
    and produce arbitrary errors.

    inheritance:

    .. inheritance-diagram:: escpos.printer.File
        :parts: 1

    """

    def __init__(self, devfile="/dev/usb/lp0", auto_flush=True, *args, **kwargs):
        """

        :param devfile: Device file under dev filesystem
        :param auto_flush: automatically call flush after every call of _raw()
        """
        Escpos.__init__(self, *args, **kwargs)
        self.devfile = devfile
        self.auto_flush = auto_flush
        self.open()

    def open(self):
        """ Open system file """
        self.device = open(self.devfile, "wb")

        if self.device is None:
            print("Could not open the specified file {0}".format(self.devfile))

    def flush(self):
        """ Flush printing content """
        self.device.flush()

    def _raw(self, msg):
        """ Print any command sent in raw format

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        self.device.write(msg)
        if self.auto_flush:
            self.flush()

    def close(self):
        """ Close system file """
        if self.device is not None:
            self.device.flush()
            self.device.close()


class Dummy(Escpos):
    """ Dummy printer

    This class is used for saving commands to a variable, for use in situations where
    there is no need to send commands to an actual printer. This includes
    generating print jobs for later use, or testing output.

    inheritance:

    .. inheritance-diagram:: escpos.printer.Dummy
        :parts: 1

    """

    def __init__(self, *args, **kwargs):
        """
        """
        Escpos.__init__(self, *args, **kwargs)
        self._output_list = []

    def _raw(self, msg):
        """ Print any command sent in raw format

        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        self._output_list.append(msg)

    @property
    def output(self):
        """ Get the data that was sent to this printer """
        return b''.join(self._output_list)

    def clear(self):
        """ Clear the buffer of the printer

        This method can be called if you send the contents to a physical printer
        and want to use the Dummy printer for new output.
        """
        del self._output_list[:]

    def close(self):
        pass
