"""Tests for Epson persistent print quality commands and responses."""

import pytest

from escpos.escpos import Escpos
from escpos.exceptions import ValidationError
from escpos.printer import LP, CupsPrinter, Dummy, File, Win32Raw

ENTER = b"\x1d(E\x03\x00\x01IN"
EXIT = b"\x1d(E\x04\x00\x02OUT"
QUERY_DENSITY = b"\x1d(E\x02\x00\x06\x05"
QUERY_SPEED = b"\x1d(E\x02\x00\x06\x06"


class ReplyPrinter(Dummy):
    """Record commands while tests provide actual reply frames through a mocked reader."""

    def _check_persistent_print_quality_support(self):
        """Use the generic raw-reader check rather than Dummy's echo-only restriction."""
        return Escpos._check_persistent_print_quality_support(self)


def reply(number, value):
    """Build a customized-setting reply with its ASCII value number."""
    return b"7'" + str(number).encode() + b"\x1f" + str(value).encode() + b"\x00"


def responses(mocker, printer, chunks):
    """Supply fragmented responses, then empty reads until the read limit."""
    chunks = iter(chunks)
    return mocker.patch.object(printer, "_read", side_effect=lambda: next(chunks, b""))


@pytest.fixture
def printer():
    """Create a printer without imposing a model whitelist."""
    return ReplyPrinter()


@pytest.mark.parametrize("name, number, query", [("density", 5, QUERY_DENSITY), ("speed", 6, QUERY_SPEED)])
@pytest.mark.parametrize("value", [0, 6, 14, 65530, 65535])
def test_save_one_setting(printer, mocker, name, number, query, value):
    """Encode the supplied parameter as a raw uint16 and verify its readback."""
    responses(mocker, printer, [b"7 \x00", reply(number, value)])

    printer.set_persistent_print_quality(**{name: value})

    assert printer.output == (
        b"\x1b@" + ENTER + b"\x1d(E\x04\x00\x05" + bytes([number]) + value.to_bytes(2, "little") + query + EXIT
    )


def test_save_both_settings_and_reset_formatting_state(printer, mocker):
    """Write one combined command and clear cached font and code page state."""
    responses(mocker, printer, [b"", b"7", b" ", b"\x00", b"", reply(5, 6), reply(6, 1)])
    printer._font = "b"
    reset_encoding = mocker.spy(printer.magic, "reset_encoding")

    printer.set_persistent_print_quality(density=6, speed=1)

    assert printer.output == (
        b"\x1b@" + ENTER + b"\x1d(E\x07\x00\x05\x05\x06\x00\x06\x01\x00" + QUERY_DENSITY + QUERY_SPEED + EXIT
    )
    assert printer._font is None
    reset_encoding.assert_called_once()


@pytest.mark.parametrize("profile", ["default", "TM-T20II", "TM-T88V"])
def test_read_is_not_restricted_to_one_printer_profile(mocker, profile):
    """Read fragmented raw values without resets, including USB empty packets."""
    printer = ReplyPrinter(profile=profile)
    printer._font = "b"
    responses(mocker, printer, [b"\x12", b"7", b"'5", b"\x1f", b"65530", b"\x00", b"", b"7'6\x1f1", b"\x00"])

    assert printer.get_persistent_print_quality() == {"density": 65530, "speed": 1}
    assert printer.output == QUERY_DENSITY + QUERY_SPEED
    assert printer._font == "b"


@pytest.mark.parametrize(
    "settings", [{}] + [{name: value} for name in ("density", "speed") for value in (-1, 65536, True, 1.5, "6")]
)
def test_invalid_setting_sends_no_commands(printer, settings):
    """Reject invalid values before any initialization or mode change."""
    with pytest.raises(ValueError):
        printer.set_persistent_print_quality(**settings)
    assert printer.output == b""


@pytest.mark.parametrize("operation", ["get", "set"])
def test_write_only_transport_sends_no_commands(printer, mocker, operation):
    """Reject transports without a read implementation before sending commands."""
    mocker.patch.object(ReplyPrinter, "_read", Escpos._read)
    with pytest.raises(NotImplementedError):
        if operation == "get":
            printer.get_persistent_print_quality()
        else:
            printer.set_persistent_print_quality(density=6)
    assert printer.output == b""


@pytest.mark.parametrize("transport", [LP, CupsPrinter, File, Dummy, Win32Raw])
@pytest.mark.parametrize("operation", ["get", "set"])
def test_transport_without_raw_replies_sends_no_commands(mocker, transport, operation):
    """Reject incompatible readers before opening any file or print queue."""
    printer = transport.__new__(transport)
    raw = mocker.patch.object(printer, "_raw")
    with pytest.raises(NotImplementedError):
        if operation == "get":
            printer.get_persistent_print_quality()
        else:
            printer.set_persistent_print_quality(density=6)
    raw.assert_not_called()


@pytest.mark.parametrize(
    "chunk",
    [b"7'5\x1f" + value + b"\x00" for value in (b"", b"-1", b"abc", b"65536", b"000001")]
    + [b"", b"7'5\x1f6", reply(6, 1), b"x" * 64],
)
def test_invalid_or_missing_response_is_bounded(printer, mocker, chunk):
    """Reject invalid values or incomplete frames within a bounded number of reads."""
    reader = responses(mocker, printer, [chunk])
    with pytest.raises(ValidationError):
        printer.get_persistent_print_quality()
    assert printer.output == QUERY_DENSITY
    assert reader.call_count <= 64


@pytest.mark.parametrize("notice", [b"", b"7 unexpected\x00"])
def test_mode_notice_failure_exits_without_nv_write(printer, mocker, notice):
    """Exit setting mode when its notice is absent or malformed."""
    responses(mocker, printer, [notice])
    with pytest.raises(ValidationError):
        printer.set_persistent_print_quality(density=6)
    assert printer.output == b"\x1b@" + ENTER + EXIT


def test_readback_mismatch_exits_without_retry(printer, mocker):
    """Exit and report a mismatching readback instead of retrying the write."""
    responses(mocker, printer, [b"7 \x00", reply(5, 5)])
    with pytest.raises(ValidationError):
        printer.set_persistent_print_quality(density=6)
    assert printer.output == b"\x1b@" + ENTER + b"\x1d(E\x04\x00\x05\x05\x06\x00" + QUERY_DENSITY + EXIT


def test_write_error_still_exits_setting_mode(printer, mocker):
    """Attempt to leave user setting mode even if its NV write fails."""
    responses(mocker, printer, [b"7 \x00"])
    raw = mocker.patch.object(printer, "_raw", side_effect=[None, None, OSError("write failed"), None])
    with pytest.raises(OSError):
        printer.set_persistent_print_quality(density=6)
    assert raw.call_args_list[-1].args == (EXIT,)
    assert raw.call_count == 4


def test_read_error_still_exits_setting_mode(printer, mocker):
    """Propagate transport errors and leave setting mode without retrying."""
    mocker.patch.object(printer, "_read", side_effect=[b"7 \x00", TimeoutError("read failed")])
    with pytest.raises(TimeoutError):
        printer.set_persistent_print_quality(density=6)
    assert printer.output.endswith(QUERY_DENSITY + EXIT)
