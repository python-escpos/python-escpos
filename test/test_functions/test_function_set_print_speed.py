import pytest

from escpos.printer import Dummy


@pytest.mark.parametrize("speed", range(1, 18))
def test_set_print_speed_accepts_valid_speed(speed):
    """Test that set_print_speed accepts valid speed values."""

    printer = Dummy()
    printer.set_print_speed(speed)

    assert printer.output == b"\x1d\x28\x4b\x02\x00\x32" + bytes([speed])


@pytest.mark.parametrize("speed", [0, 18])
def test_set_print_speed_rejects_out_of_bounds_speed(speed):
    """Test that set_print_speed raises ValueError for out-of-bounds speed values."""

    printer = Dummy()

    with pytest.raises(ValueError):
        printer.set_print_speed(speed)
