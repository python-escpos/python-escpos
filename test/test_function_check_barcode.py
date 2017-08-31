#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import escpos.printer as printer
import pytest


def test_barcode_upca():
    bc = 'UPC-A'

    valid_codes = [
        "01234567890",
        "012345678905"
    ]

    invalid_codes = [
        "01234567890123",   # too long
        "0123456789",       # too short
        "72527273-711",     # invalid '-'
        "A12345678901",     # invalid 'A'
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_upce():
    bc = 'UPC-E'

    valid_codes = [
        "01234567",
        "0123456",
        "012345678905"
    ]
    invalid_codes = [
        "01234567890123",  # too long
        "012345",          # too short
        "72527-2",         # invalid '-'
        "A123456",         # invalid 'A'
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_ean13():
    bc = 'EAN13'

    valid_codes = [
        "0123456789012",
        "012345678901"
    ]
    invalid_codes = [
        "0123456789",       # too short
        "A123456789012"     # invalid 'A'
        "012345678901234",  # too long
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_ean8():
    bc = 'EAN8'

    valid_codes = [
        "01234567",
        "0123456"
    ]
    invalid_codes = [
        "012345",           # too short
        "A123456789012"     # invalid 'A'
        "012345678901234",  # too long
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_code39():
    bc = 'CODE39'

    valid_codes = [
        "ABC-1234",
        "ABC-1234-$$-+A",
        "*WIKIPEDIA*"  # the '*' symbol is not part of the actual code, but it is handled properly by ESCPOS
    ]
    invalid_codes = [
        "ALKJ_34",  # invalid '_'
        "A" * 256,  # too long
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_itf():
    bc = 'ITF'

    valid_codes = [
        "010203040506070809",
        "11221133113344556677889900",
    ]
    invalid_codes = [
        "010203040",  # odd length
        "0" * 256,    # too long
        "AB01",       # invalid 'A'
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_codabar():
    bc = 'CODABAR'

    valid_codes = [
        "A2030405060B",
        "C11221133113344556677889900D",
        "D0D",
    ]
    invalid_codes = [
        "010203040",  # no start/stop
        "0" * 256,    # too long
        "AB-01F",     # invalid 'B'
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_nw7():
    bc = 'NW7'  # same as CODABAR

    valid_codes = [
        "A2030405060B",
        "C11221133113344556677889900D",
        "D0D",
    ]
    invalid_codes = [
        "010203040",  # no start/stop
        "0" * 256,    # too long
        "AB-01F",     # invalid 'B'
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_code93():
    bc = 'CODE93'

    valid_codes = [
        "A2030405060B",
        "+:$&23-7@$",
        "D0D",
    ]
    invalid_codes = [
        "é010203040",  # invalid 'é'
        "0" * 256,     # too long
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_code128():
    bc = 'CODE128'

    valid_codes = [
        "{A2030405060B",
        "{C+:$&23-7@$",
        "{B0D",
    ]
    invalid_codes = [
        "010203040",  # missing leading {
        "0" * 256,    # too long
        "{D2354AA",   # second char not between A-C
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_gs1_128():
    bc = 'GS1-128'  # same as code 128

    valid_codes = [
        "{A2030405060B",
        "{C+:$&23-7@$",
        "{B0D",
    ]
    invalid_codes = [
        "010203040",  # missing leading {
        "0" * 256,    # too long
        "{D2354AA",   # second char not between A-C
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_gs1_omni():
    bc = 'GS1 DATABAR OMNIDIRECTIONAL'

    valid_codes = [
        "0123456789123",
    ]
    invalid_codes = [
        "01234567891234",  # too long
        "012345678912",    # too short
        "012345678A1234",  # invalid 'A'
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_gs1_trunc():
    bc = 'GS1 DATABAR TRUNCATED'  # same as OMNIDIRECTIONAL

    valid_codes = [
        "0123456789123",
    ]
    invalid_codes = [
        "01234567891234",  # too long
        "012345678912",    # too short
        "012345678A1234",  # invalid 'A'
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_gs1_limited():
    bc = 'GS1 DATABAR LIMITED'

    valid_codes = [
        "0123456789123",
        "0123456789123",
    ]
    invalid_codes = [
        "01234567891234",  # too long
        "012345678912",    # too short
        "012345678A1234",  # invalid 'A'
        "02345678912341",  # invalid start (should be 01)
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))


def test_barcode_gs1_expanded():
    bc = 'GS1 DATABAR EXPANDED'

    valid_codes = [
        "(9A{A20304+-%&06a0B",
        "(1 {C+:$a23-7%",
        "(00000001234567678",
    ]
    invalid_codes = [
        "010203040",     # missing leading {
        "0" * 256,       # too long
        "0{D2354AA",     # second char not between A-za-z0-9
        "IT will fail",  # first char not between 0-9
    ]

    assert (all([printer.Escpos.check_barcode(bc, code) for code in valid_codes]))
    assert (not any([printer.Escpos.check_barcode(bc, code) for code in invalid_codes]))
