#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""This module contains the implementation of the CupsPrinter printer driver.

:author: python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2012-2023 Bashlinux and python-escpos
:license: MIT
"""

from ..escpos import Escpos

_CUPSPRINT = False
try:
    import tempfile

    import cups

    _CUPSPRINT = True
except ImportError:
    pass

if _CUPSPRINT:

    class CupsPrinter(Escpos):
        """Simple CUPS printer connector.

        .. note::

            Requires ``pycups`` which in turn needs the cups development library package:
                - Ubuntu/Debian: ``libcups2-dev``
                - OpenSuse/Fedora: ``cups-devel``

        inheritance:

        .. inheritance-diagram:: escpos.printer.CupsPrinter
            :parts: 1

        """

        def __init__(self, printer_name=None, *args, **kwargs):
            """Class constructor for CupsPrinter.

            :param printer_name: CUPS printer name (Optional)
            :type printer_name: str
            :param host: CUPS server host/ip (Optional)
            :type host: str
            :param port: CUPS server port (Optional)
            :type port: int
            """
            Escpos.__init__(self, *args, **kwargs)
            host, port = args or (
                kwargs.get("host", cups.getServer()),
                kwargs.get("port", cups.getPort()),
            )
            cups.setServer(host)
            cups.setPort(port)
            self.conn = cups.Connection()
            self.tmpfile = None
            self.printer_name = printer_name
            self.job_name = ""
            self.pending_job = False
            self.open()

        @property
        def printers(self):
            """Available CUPS printers."""
            return self.conn.getPrinters()

        def open(self, job_name="python-escpos"):
            """Set up a new print job and target the printer.

            A call to this method is required to send new jobs to
            the same CUPS connection.

            Defaults to default CUPS printer.
            Creates a new temporary file buffer.
            """
            self.job_name = job_name
            if self.printer_name not in self.printers:
                self.printer_name = self.conn.getDefault()
            self.tmpfile = tempfile.NamedTemporaryFile(delete=True)

        def _raw(self, msg):
            """Append any command sent in raw format to temporary file.

            :param msg: arbitrary code to be printed
            :type msg: bytes
            """
            self.pending_job = True
            try:
                self.tmpfile.write(msg)
            except ValueError:
                self.pending_job = False
                raise ValueError("Printer job not opened")

        def send(self):
            """Send the print job to the printer."""
            if self.pending_job:
                # Rewind tempfile
                self.tmpfile.seek(0)
                # Print temporary file via CUPS printer.
                self.conn.printFile(
                    self.printer_name,
                    self.tmpfile.name,
                    self.job_name,
                    {"document-format": cups.CUPS_FORMAT_RAW},
                )
            self._clear()

        def _clear(self):
            """Finish the print job.

            Remove temporary file.
            """
            self.tmpfile.close()
            self.pending_job = False

        def _read(self):
            """Return a single-item array with the accepting state of the print queue.

            states: idle = [3], printing a job = [4], stopped = [5]
            """
            printer = self.printers.get(self.printer_name, {})
            state = printer.get("printer-state")
            if not state:
                return []
            return [state]

        def close(self):
            """Close CUPS connection.

            Send pending job to the printer if needed.
            """
            if self.pending_job:
                self.send()
            if self.conn:
                print("Closing CUPS connection to printer {}".format(self.printer_name))
                self.conn = None
