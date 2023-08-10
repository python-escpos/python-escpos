import pytest
import six

from escpos import printer
from escpos.constants import BUZZER


def test_buzzer_function_with_default_params():
    instance = printer.Dummy()
    instance.buzzer()
    expected = BUZZER + six.int2byte(2) + six.int2byte(4)
    assert instance.output == expected


@pytest.mark.parametrize(
    "times, duration",
    [
        [1, 1],
        [2, 2],
        [3, 3],
        [4, 4],
        [5, 5],
        [6, 6],
        [7, 7],
        [8, 8],
        [9, 9],
    ],
)
def test_buzzer_function(times, duration):
    instance = printer.Dummy()
    instance.buzzer(times, duration)
    expected = BUZZER + six.int2byte(times) + six.int2byte(duration)
    assert instance.output == expected


@pytest.mark.parametrize(
    "times, duration, expected_message",
    [
        [0, 0, "times must be between 1 and 9"],
        [-1, 0, "times must be between 1 and 9"],
        [10, 0, "times must be between 1 and 9"],
        [11, 0, "times must be between 1 and 9"],
        [3, 0, "duration must be between 1 and 9"],
        [3, -1, "duration must be between 1 and 9"],
        [3, 10, "duration must be between 1 and 9"],
        [3, 11, "duration must be between 1 and 9"],
    ],
)
def test_buzzer_fuction_with_outrange_values(times, duration, expected_message):
    instance = printer.Dummy()
    with pytest.raises(ValueError) as e:
        instance.buzzer(times, duration)

    assert str(e.value) == expected_message
