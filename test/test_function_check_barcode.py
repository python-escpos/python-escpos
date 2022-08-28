#!/usr/bin/python
# -*- coding: utf-8 -*-


import escpos.printer as printer
import pytest


@pytest.mark.parametrize(
    "bctype,data",
    [
        ("UPC-A", "01234567890"),
        ("UPC-A", "012345678905"),
        ("UPC-E", "01234567"),
        ("UPC-E", "0123456"),
        ("UPC-E", "012345678905"),
        ("EAN13", "0123456789012"),
        ("EAN13", "012345678901"),
        ("EAN8", "01234567"),
        ("EAN8", "0123456"),
        ("CODE39", "ABC-1234"),
        ("CODE39", "ABC-1234-$$-+A"),
        ("CODE39", "*WIKIPEDIA*"),
        ("ITF", "010203040506070809"),
        ("ITF", "11221133113344556677889900"),
        ("CODABAR", "A2030405060B"),
        ("CODABAR", "C11221133113344556677889900D"),
        ("CODABAR", "D0D"),
        ("NW7", "A2030405060B"),
        ("NW7", "C11221133113344556677889900D"),
        ("NW7", "D0D"),
        ("CODE93", "A2030405060B"),
        ("CODE93", "+:$&23-7@$"),
        ("CODE93", "D0D"),
        ("CODE128", "{A2030405060B"),
        ("CODE128", "{C+:$&23-7@$"),
        ("CODE128", "{B0D"),
        ("GS1-128", "{A2030405060B"),
        ("GS1-128", "{C+:$&23-7@$"),
        ("GS1-128", "{B0D"),
        ("GS1 DATABAR OMNIDIRECTIONAL", "0123456789123"),
        ("GS1 DATABAR TRUNCATED", "0123456789123"),
        ("GS1 DATABAR LIMITED", "0123456789123"),
        ("GS1 DATABAR EXPANDED", "(9A{A20304+-%&06a0B"),
        ("GS1 DATABAR EXPANDED", "(1 {C+:&23-7%"),
        ("GS1 DATABAR EXPANDED", "(00000001234567678"),
    ],
)
def test_check_valid_barcode(bctype, data):
    assert printer.Escpos.check_barcode(bctype, data)


@pytest.mark.parametrize(
    "bctype,data",
    [
        ("UPC-A", "01234567890123"),  # too long
        ("UPC-A", "0123456789"),  # too short
        ("UPC-A", "72527273-711"),  # invalid '-'
        ("UPC-A", "A12345678901"),  # invalid 'A'
        ("UPC-E", "01234567890123"),  # too long
        ("UPC-E", "012345"),  # too short
        ("UPC-E", "72527-2"),  # invalid '-'
        ("UPC-E", "A123456"),  # invalid 'A'
        ("EAN13", "0123456789"),  # too short
        ("EAN13", "A123456789012"),  # invalid 'A'
        ("EAN13", "012345678901234"),  # too long
        ("EAN8", "012345"),  # too short
        ("EAN8", "A123456789012"),  # invalid 'A'
        ("EAN8", "012345678901234"),  # too long
        ("CODE39", "ALKJ_34"),  # invalid '_'
        ("CODE39", "A" * 256),  # too long
        ("ITF", "010203040"),  # odd length
        ("ITF", "0" * 256),  # too long
        ("ITF", "AB01"),  # invalid 'A'
        ("CODABAR", "010203040"),  # no start/stop
        ("CODABAR", "0" * 256),  # too long
        ("CODABAR", "AB-01F"),  # invalid 'B'
        ("NW7", "010203040"),  # no start/stop
        ("NW7", "0" * 256),  # too long
        ("NW7", "AB-01F"),  # invalid 'B'
        ("CODE93", "é010203040"),  # invalid 'é'
        ("CODE93", "0" * 256),  # too long
        ("CODE128", "010203040"),  # missing leading {
        ("CODE128", "{D2354AA"),  # second char not between A-C
        ("CODE128", "0" * 256),  # too long
        ("GS1-128", "010203040"),  # missing leading {
        ("GS1-128", "{D2354AA"),  # second char not between A-C
        ("GS1-128", "0" * 256),  # too long
        ("GS1 DATABAR OMNIDIRECTIONAL", "01234567891234"),  # too long
        ("GS1 DATABAR OMNIDIRECTIONAL", "012345678912"),  # too short
        ("GS1 DATABAR OMNIDIRECTIONAL", "012345678A1234"),  # invalid 'A'
        ("GS1 DATABAR TRUNCATED", "01234567891234"),  # too long
        ("GS1 DATABAR TRUNCATED", "012345678912"),  # too short
        ("GS1 DATABAR TRUNCATED", "012345678A1234"),  # invalid 'A'
        ("GS1 DATABAR LIMITED", "01234567891234"),  # too long
        ("GS1 DATABAR LIMITED", "012345678912"),  # too short
        ("GS1 DATABAR LIMITED", "012345678A1234"),  # invalid 'A'
        ("GS1 DATABAR LIMITED", "02345678912341"),  # invalid start (should be 01)
        ("GS1 DATABAR EXPANDED", "010203040"),  # missing leading (
        ("GS1-128", "(" + ("0" * 256)),  # too long
        ("GS1 DATABAR EXPANDED", "(a{D2354AA"),  # second char not between 0-9
        ("GS1 DATABAR EXPANDED", "IT will fail"),  # first char not '('
    ],
)
def test_check_invalid_barcode(bctype, data):
    assert not printer.Escpos.check_barcode(bctype, data)
