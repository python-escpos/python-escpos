#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for software_columns

:author: Benito López and the python-escpos developers
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2024 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


import pytest


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
@pytest.mark.parametrize(
    "align", [["center", "center", "center"], ["center"], "center"]
)
def test_software_columns_valid_args(driver, text_list, widths, align) -> None:
    """
    GIVEN a dummy printer object
    WHEN valid params are passed
    THEN check no errors
    """
    driver.software_columns(text_list=text_list, widths=widths, align=align)
    driver.close()
