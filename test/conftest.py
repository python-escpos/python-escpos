import pytest

from escpos.exceptions import DeviceNotFoundError
from escpos.printer import LP, CupsPrinter, Dummy, File, Network, Serial, Usb, Win32Raw


@pytest.fixture
def driver():
    return Dummy()


@pytest.fixture
def usbprinter():
    return Usb()


@pytest.fixture
def serialprinter():
    return Serial()


@pytest.fixture
def networkprinter():
    return Network()


@pytest.fixture
def fileprinter():
    return File()


@pytest.fixture
def lpprinter():
    return LP()


@pytest.fixture
def win32rawprinter():
    return Win32Raw()


@pytest.fixture
def cupsprinter():
    return CupsPrinter()


@pytest.fixture
def devicenotfounderror():
    return DeviceNotFoundError
