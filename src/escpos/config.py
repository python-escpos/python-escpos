"""ESC/POS configuration manager.

This module contains the implementations of abstract base class :py:class:`Config`.
"""

import os
import pathlib

import platformdirs
import yaml

from . import exceptions, printer


class Config:
    """Configuration handler class.

    This class loads configuration from a default or specified directory. It
    can create your defined printer and return it to you.
    """

    _app_name = "python-escpos"
    _config_file = "config.yaml"

    def __init__(self) -> None:
        """Initialize configuration.

        Remember to add anything that needs to be reset between configurations
        to self._reset_config
        """
        self._has_loaded = False
        self._printer = None

        self._printer_name = ""
        self._printer_config = None

    def _reset_config(self) -> None:
        """Clear the loaded configuration.

        If we are loading a changed config, we don't want to have leftover
        data.
        """
        self._has_loaded = False
        self._printer = None
        self._printer_name = ""
        self._printer_config = None

    def _set_config(self, config) -> None:
        """Set configuration variables.

        :param config: config object loaded from file or string.
        """
        self._printer_config = config.get("printer", None)
        if self._printer_config is None:
            self._has_loaded = True
            return
        printer_name = self._printer_config.get("type", "")
        class_names = {
            "usb": "Usb",
            "serial": "Serial",
            "network": "Network",
            "file": "File",
            "dummy": "Dummy",
            "cupsprinter": "CupsPrinter",
            "lp": "LP",
            "win32raw": "Win32Raw",
        }
        self._printer_name = class_names.get(printer_name.lower(), printer_name)
        if not self._printer_name or not hasattr(printer, self._printer_name):
            raise exceptions.ConfigSyntaxError(
                f'Printer type "{self._printer_name}" is invalid'
            )

        self._has_loaded = True

    def load(self, config_path=None) -> None:
        """Load and parse the configuration file using pyyaml.

        :param config_path: An optional file path, file handle, or byte string
            for the configuration file.
        """

        if not config_path:
            config_path = os.path.join(
                platformdirs.user_config_dir(self._app_name), self._config_file
            )
        if isinstance(config_path, pathlib.Path):
            # store string if posixpath
            config_path = config_path.as_posix()
        if not os.path.isfile(config_path):
            # supplied path is not a file --> assume default file
            config_path = os.path.join(config_path, self._config_file)

        try:
            with open(config_path, "rb") as config_file:
                self.load_yaml_string(config_file)
        except EnvironmentError:
            raise exceptions.ConfigNotFoundError(
                f"Couldn't read config at {config_path}"
            )

    def load_yaml_string(self, yaml_string) -> None:
        """Load and parse a yaml configuration string or file-like object.

        :param yaml_string: A string or file-like object containing yaml formatted configuration.
        """
        self._reset_config()

        try:
            config = yaml.safe_load(yaml_string)
        except yaml.YAMLError:
            raise exceptions.ConfigSyntaxError("Error parsing YAML")

        self._set_config(config)

    def printer(self):
        """Return a printer that was defined in the config.

        Throw an exception on error.

        This method loads the default config if one has not been already loaded.

        """
        if not self._has_loaded:
            self.load()

        if not self._printer_name:
            raise exceptions.ConfigSectionMissingError("printer")

        if not self._printer:
            # We could catch init errors and make them a ConfigSyntaxError,
            # but I'll just let them pass
            self._printer = getattr(printer, self._printer_name)(**self._printer_config)

        return self._printer
