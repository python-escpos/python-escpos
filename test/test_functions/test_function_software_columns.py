#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for software_columns

:author: Benito López and the python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2024 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import pytest


def test_rearrange_into_cols(driver) -> None:
    """
    GIVEN a list of columnable text
    WHEN the column width is different for each column and some strings exceed the max width
    THEN check the strings are properly wrapped, truncated and rearranged into some columns
    """

    output = driver._rearrange_into_cols(
        text_list=["fits", "row1 row2", "truncate and wrap"], widths=[4, 5, 6]
    )
    assert output == [["fits", "row1", "trunc."], ["", "row2", "and"], ["", "", "wrap"]]


def test_add_padding_into_cols(driver) -> None:
    """
    GIVEN a list of strings
    WHEN adding padding and different alignments to each string
    THEN check the strings are correctly padded and aligned
    """

    output = driver._add_padding_into_cols(
        text_list=["col1", "col2", "col3", "col 4"],
        widths=[6, 6, 6, 6],
        align=["center", "left", "right", "justify"],
    )
    assert output == [" col1 ", "col2  ", "  col3", "col  4"]


@pytest.mark.parametrize("text_list", ["", [], None])
@pytest.mark.parametrize("widths", [30.5, "30", None])
@pytest.mark.parametrize("align", ["invalid_align_name", "", None])
def test_software_columns_invalid_args(driver, text_list, widths, align) -> None:
    """
    GIVEN a dummy printer object
    WHEN non valid params are passed
    THEN check raise exception
    """
    bad_text_list = {"text_list": text_list, "widths": 5, "align": "left"}
    bad_widths = {"text_list": ["valid"], "widths": widths, "align": "left"}
    bad_align = {"text_list": ["valid"], "widths": 5, "align": align}

    bad_args = [bad_text_list, bad_widths, bad_align]
    for kwargs in bad_args:
        with pytest.raises(Exception):
            driver.software_columns(**kwargs)
        driver.close()


@pytest.mark.parametrize(
    "text_list",
    [
        ["col1", "col2", "col3"],
        ["wrap this string", "wrap this string", "wrap this string"],
        ["truncate_this_string", "truncate_this_string", "truncate_this_string"],
    ],
)
@pytest.mark.parametrize("widths", [[10, 10, 10], [10], 30])
@pytest.mark.parametrize("align", [["center", "left", "right"], ["center"], "justify"])
def test_software_columns_valid_args(driver, text_list, widths, align) -> None:
    """
    GIVEN a dummy printer object
    WHEN valid params are passed
    THEN check no errors
    """
    driver.software_columns(text_list=text_list, widths=widths, align=align)
    driver.close()
