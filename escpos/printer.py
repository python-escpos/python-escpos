#!/usr/bin/python
"""
@author: Manuel F Martinez <manpaz@bashlinux.com>
@organization: Bashlinux
@copyright: Copyright (c) 2012 Bashlinux
@license: GPL
"""

import usb.core
import usb.util
import serial
import socket

from escpos import *
from constants import *
from exceptions import *

class Usb(Escpos):
    """ Define USB printer """

    is_open = False

    def __init__(self, idVendor, idProduct, interface=0, in_ep=0x82, out_ep=0x01):
        """
        @param idVendor  : Vendor ID
        @param idProduct : Product ID
        @param interface : USB device interface
        @param in_ep     : Input end point
        @param out_ep    : Output end point
        """
        self.idVendor  = idVendor
        self.idProduct = idProduct
        self.interface = interface
        self.in_ep     = in_ep
        self.out_ep    = out_ep
        self.open()


    def open(self):
        """ Search device on USB tree and set is as escpos device """
        if self.is_open:
            return  # Already open; no need to reopen

        self.device = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct)
        if self.device is None:
            print "Cable isn't plugged in"
        else:
            self.is_open = True

        if self.device.is_kernel_driver_active(0):
            try:
                self.device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                print "Could not detatch kernel driver: %s" % str(e)

        try:
            self.device.set_configuration()
            self.device.reset()
        except usb.core.USBError as e:
            # Seems fatal when it occurs. Should the device be closed as a result?
            #self.close()
            print "Could not set configuration: %s" % str(e)


    def close(self):
        """ Manually release USB interface """
        self.is_open = False

        if self.device:
            usb.util.dispose_resources(self.device)

        self.device = None


    def _raw(self, msg):
        """ Print any command sent in raw format """
        self.device.write(self.out_ep, msg, self.interface)


    def __del__(self):
        """ Release USB interface """
        self.close()



class Serial(Escpos):
    """ Define Serial printer """

    is_open = False

    def __init__(self, devfile="/dev/ttyS0", baudrate=9600, bytesize=8, timeout=1):
        """
        @param devfile  : Device file under dev filesystem
        @param baudrate : Baud rate for serial transmission
        @param bytesize : Serial buffer size
        @param timeout  : Read/Write timeout
        """
        self.devfile  = devfile
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.timeout  = timeout
        self.open()


    def open(self):
        """ Setup serial port and set it as escpos device """
        if self.is_open:
            return  # Already open; no need to reopen

        self.device = serial.Serial(port=self.devfile, baudrate=self.baudrate, bytesize=self.bytesize, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=self.timeout, dsrdtr=True)

        if self.device is not None:
            print "Serial printer enabled"
            self.is_open = True
        else:
            print "Unable to open serial printer on: %s" % self.devfile


    def close(self):
        """ Manually close Serial interface """
        self.is_open = False

        if self.device is not None:
            self.device.close()

        self.device = None


    def _raw(self, msg):
        """ Print any command sent in raw format """
        self.device.write(msg)


    def __del__(self):
        """ Close Serial interface """
        self.close()


class Network(Escpos):
    """ Define Network printer """

    is_open = False

    def __init__(self,host,port=9100):
        """
        @param host : Printer's hostname or IP address
        @param port : Port to write to
        """
        self.host = host
        self.port = port
        self.open()


    def open(self):
        """ Open TCP socket and set it as escpos device """
        if self.is_open:
            return  # Already open; no need to reopen

        self.device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device.connect((self.host, self.port))

        if self.device is None:
            print "Could not open socket for %s" % self.host
        else:
            self.is_open = True


    def close(self):
        """ Manually close TCP connection """
        self.is_open = False

        if self.device is not None:
            self.device.close()

        self.device = None


    def _raw(self, msg):
        """ Print any command sent in raw format """
        self.device.send(msg)


    def __del__(self):
        """ Close TCP connection """
        self.close()



class File(Escpos):
    """ Define Generic file printer """

    is_open = False

    def __init__(self, devfile="/dev/usb/lp0"):
        """
        @param devfile : Device file under dev filesystem
        """
        self.devfile = devfile
        self.open()


    def open(self):
        """ Open system file """
        if self.is_open:
            return  # Already open; no need to reopen

        self.device = open(self.devfile, "wb")

        if self.device is None:
            print "Could not open the specified file %s" % self.devfile
        else:
            self.is_open = True


    def close(self):
        """ Manually close system file """
        self.is_open = False

        if self.device is not None:
            self.device.close()

        self.device = None


    def _raw(self, msg):
        """ Print any command sent in raw format """
        self.device.write(msg);


    def __del__(self):
        """ Close system file """
        self.close()
