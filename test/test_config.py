#!/usr/bin/python
"""tests for config module

:author: `Patrick Kanzler <dev@pkanzler.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2023 `python-escpos <https://github.com/python-escpos>`_
:license: MIT
"""


def generate_dummy_config(path):
    """Generate a dummy config in path"""
    dummy_config_content = "printer:\n   type: Dummy\n"
    path.write_text(dummy_config_content)
    assert path.read_text() == dummy_config_content


def test_config_load_with_file(tmp_path):
    """Test the loading of a config with a config file."""
    # generate a dummy config
    config_file = tmp_path / "config.yaml"
    generate_dummy_config(config_file)

    # test the config loading
    from escpos import config

    c = config.Config()
    c.load(config_path=config_file)
    print(c._printer_config)

    # test the resulting printer object
    p = c.printer()
    p._raw(b"1234")

    assert p.output == b"1234"


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
    p = c.printer()
    p._raw(b"1234")

    assert p.output == b"1234"
