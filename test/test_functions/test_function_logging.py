"""Regression tests for https://github.com/python-escpos/python-escpos/issues/675.

The library must not write diagnostics with ``print()`` (which callers cannot
suppress). All runtime diagnostics go through the :mod:`logging` module so
users can silence or redirect them with standard logging configuration.
"""

import logging

from PIL import Image

import escpos.printer as printer


def _records(caplog, level: int):
    """Log records from the escpos logger at the given level."""
    return [
        r for r in caplog.records if r.name == "escpos.escpos" and r.levelno == level
    ]


def _dummy_with_unknown_width() -> printer.Dummy:
    instance = printer.Dummy()
    instance.profile.profile_data = {"media": {"width": {"pixels": "Unknown"}}}
    return instance


def test_image_without_center_is_silent(capsys, caplog) -> None:
    """No warning when centering was not requested, and nothing on stdout."""
    instance = _dummy_with_unknown_width()
    with caplog.at_level(logging.WARNING, logger="escpos.escpos"):
        instance.image(Image.new("RGB", (10, 10)), center=False)
    assert capsys.readouterr().out == ""
    assert "media.width.pixel" not in caplog.text


def test_image_with_center_missing_width_key_logs_warning(capsys, caplog) -> None:
    """Missing width key warns when centering, stays silent otherwise."""
    for center, expect_warning in ((True, True), (False, False)):
        instance = printer.Dummy()
        instance.profile.profile_data = {"media": {}}
        caplog.clear()
        with caplog.at_level(logging.WARNING, logger="escpos.escpos"):
            instance.image(Image.new("RGB", (10, 10)), center=center)
        assert capsys.readouterr().out == ""
        warnings = _records(caplog, logging.WARNING)
        assert (
            any("media.width.pixel" in r.getMessage() for r in warnings)
            is expect_warning
        )


def test_image_with_center_logs_warning_not_stdout(capsys, caplog) -> None:
    """Centering without known width logs a warning instead of printing."""
    instance = _dummy_with_unknown_width()
    with caplog.at_level(logging.WARNING, logger="escpos.escpos"):
        instance.image(Image.new("RGB", (10, 10)), center=True)
    assert capsys.readouterr().out == ""
    assert any(
        "media.width.pixel" in r.getMessage() for r in _records(caplog, logging.WARNING)
    )


def test_barcode_renderer_choice_logs_not_prints(capsys, caplog) -> None:
    """Renderer selection is logged at INFO level, stdout stays empty."""
    instance = printer.Dummy()
    with caplog.at_level(logging.INFO, logger="escpos.escpos"):
        instance.barcode("123456789012", "EAN13")
    assert capsys.readouterr().out == ""
    assert any(
        "barcode renderer" in r.getMessage() for r in _records(caplog, logging.INFO)
    )


def test_software_barcode_renderer_logs_not_prints(capsys, caplog) -> None:
    """Forced software renderer is logged, stdout stays empty."""
    instance = printer.Dummy()
    with caplog.at_level(logging.INFO, logger="escpos.escpos"):
        instance.barcode("123456789012", "EAN13", force_software=True)
    assert capsys.readouterr().out == ""
    assert any(
        "software barcode renderer" in r.getMessage()
        for r in _records(caplog, logging.INFO)
    )


def test_software_barcode_string_impl_logs_not_prints(capsys, caplog) -> None:
    """Explicit software renderer selection is logged, stdout stays empty."""
    instance = printer.Dummy()
    with caplog.at_level(logging.INFO, logger="escpos.escpos"):
        instance.barcode("123456789012", "EAN13", force_software="graphics")
    assert capsys.readouterr().out == ""
    assert any(
        "Using graphics software barcode renderer" in r.getMessage()
        for r in _records(caplog, logging.INFO)
    )


def test_dpi_fallback_logs_warning_not_stdout(capsys, caplog) -> None:
    """Missing DPI info logs a warning instead of printing."""
    instance = printer.Dummy()
    instance.profile.profile_data = {"media": {}}
    with caplog.at_level(logging.WARNING, logger="escpos.escpos"):
        assert instance._dpi() == 180
    assert capsys.readouterr().out == ""
    assert any("DPI" in r.getMessage() for r in _records(caplog, logging.WARNING))
