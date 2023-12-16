#!/usr/bin/python
"""tests for config module

:author: `Patrick Kanzler <dev@pkanzler.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2023 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""
import pathlib

import appdirs
import pytest

import escpos.exceptions


def generate_dummy_config(path, content=None):
    """Generate a dummy config in path"""
    dummy_config_content = content
    if not content:
        dummy_config_content = "printer:\n   type: Dummy\n"
    path.write_text(dummy_config_content)
    assert path.read_text() == dummy_config_content


def simple_printer_test(config):
    """Simple test for the dummy printer."""
    p = config.printer()
    p._raw(b"1234")

    assert p.output == b"1234"


def test_config_load_with_invalid_config_yaml(tmp_path):
    """Test the loading of a config with a invalid config file (yaml issue)."""
    # generate a dummy config
    config_file = tmp_path / "config.yaml"
    generate_dummy_config(config_file, content="}invalid}yaml}")

    # test the config loading
    from escpos import config

    c = config.Config()
    with pytest.raises(escpos.exceptions.ConfigSyntaxError):
        c.load(config_path=config_file)


def test_config_load_with_invalid_config_content(tmp_path):
    """Test the loading of a config with a invalid config file (content issue)."""
    # generate a dummy config
    config_file = tmp_path / "config.yaml"
    generate_dummy_config(
        config_file, content="printer:\n   type: NoPrinterWithThatName\n"
    )

    # test the config loading
    from escpos import config

    c = config.Config()
    with pytest.raises(escpos.exceptions.ConfigSyntaxError):
        c.load(config_path=config_file)


def test_config_load_with_missing_config(tmp_path):
    """Test the loading of a config that does not exist."""
    # test the config loading
    from escpos import config

    c = config.Config()
    with pytest.raises(escpos.exceptions.ConfigNotFoundError):
        c.load(config_path=tmp_path)


@pytest.mark.skip(
    "This test creates in the actual appdir files and is therefore skipped."
)
def test_config_load_from_appdir() -> None:
    """Test the loading of a config in appdir."""
    from escpos import config

    # generate a dummy config
    config_file = (
        pathlib.Path(appdirs.user_config_dir(config.Config._app_name))
        / config.Config._config_file
    )

    generate_dummy_config(config_file)

    # test the config loading
    c = config.Config()
    c.load()

    # test the resulting printer object
    simple_printer_test(c)


def test_config_load_with_file(tmp_path):
    """Test the loading of a config with a config file."""
    # generate a dummy config
    config_file = tmp_path / "config.yaml"
    generate_dummy_config(config_file)

    # test the config loading
    from escpos import config

    c = config.Config()
    c.load(config_path=config_file)

    # test the resulting printer object
    simple_printer_test(c)


def test_config_load_with_path(tmp_path):
    """Test the loading of a config with a config path."""
    # generate a dummy config
    config_file = tmp_path / "config.yaml"
    generate_dummy_config(config_file)

    # test the config loading
    from escpos import config

    c = config.Config()
    c.load(config_path=tmp_path)

    # test the resulting printer object
    simple_printer_test(c)
