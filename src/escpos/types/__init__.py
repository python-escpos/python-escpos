# -*- coding: utf-8 -*-
"""Custom types."""

from typing import Dict, TypedDict


class ConstTxtStyleClass(TypedDict):
    """Describe type of :py:data:`escpos.constants.TXT_STYLES`."""

    bold: Dict[bool, bytes]
    underline: Dict[int, bytes]
    size: Dict[str, bytes]
    font: Dict[str, bytes]
    align: Dict[str, bytes]
    invert: Dict[bool, bytes]
    color: Dict[str, bytes]
    flip: Dict[bool, bytes]
    density: Dict[int, bytes]
    smooth: Dict[bool, bytes]
    height: Dict[int, int]
    width: Dict[int, int]
