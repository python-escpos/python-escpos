#!/usr/bin/python

import escpos.printer as printer
import pytest
import mock
import socket


@pytest.fixture
def instance():
    socket.socket.connect = mock.Mock()
    return printer.Network("localhost")


def test_close_without_open(instance):
    """try to close without opening (should fail gracefully)

    Currently we never open from our fixture, so calling close once
    should be enough. In the future this might not be enough,
    therefore we have to close twice in order to provoke an error
    (if possible, this should not raise)
    """
    instance.close()
    instance.close()
