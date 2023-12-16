import pytest

from escpos.exceptions import DeviceNotFoundError
from escpos.printer import LP, CupsPrinter, Dummy, File, Network, Serial, Usb, Win32Raw


@pytest.fixture
def driver() -> Dummy:
    return Dummy()


@pytest.fixture
def usbprinter() -> Usb:
    return Usb()


@pytest.fixture
def serialprinter() -> Serial:
    return Serial()


@pytest.fixture
def networkprinter() -> Network:
    return Network()


@pytest.fixture
def fileprinter() -> File:
    return File()


@pytest.fixture
def lpprinter() -> LP:
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
