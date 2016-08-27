import pytest
from escpos.printer import Dummy


@pytest.fixture
def driver():
    return Dummy()
