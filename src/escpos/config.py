""" ESC/POS configuration manager.

This module contains the implementations of abstract base class :py:class:`Config`.

"""


import os
import appdirs
import yaml

from . import printer
from . import exceptions


class Config(object):
    """Configuration handler class.

    This class loads configuration from a default or specificed directory. It
    can create your defined printer and return it to you.
    """

    _app_name = "python-escpos"
    _config_file = "config.yaml"

    def __init__(self):
        """Initialize configuration.

        Remember to add anything that needs to be reset between configurations
        to self._reset_config
        """
        self._has_loaded = False
        self._printer = None

        self._printer_name = None
        self._printer_config = None

    def _reset_config(self):
        """Clear the loaded configuration.

        If we are loading a changed config, we don't want to have leftover
        data.
        """
        self._has_loaded = False
        self._printer = None

        self._printer_name = None
        self._printer_config = None

    def load(self, config_path=None):
        """Load and parse the configuration file using pyyaml

        :param config_path: An optional file path, file handle, or byte string
            for the configuration file.

        """

        self._reset_config()

        if not config_path:
            config_path = os.path.join(
                appdirs.user_config_dir(self._app_name), self._config_file
            )

        try:
            # First check if it's file like. If it is, pyyaml can load it.
            # I'm checking type instead of catching exceptions to keep the
            # exception handling simple
            if hasattr(config_path, "read"):
                config = yaml.safe_load(config_path)
            else:
                # If it isn't, it's a path. We have to open it first, otherwise
                # pyyaml will try to read it as yaml
                with open(config_path, "rb") as config_file:
                    config = yaml.safe_load(config_file)
        except EnvironmentError:
            raise exceptions.ConfigNotFoundError(
                "Couldn't read config at {config_path}".format(
                    config_path=str(config_path),
                )
            )
        except yaml.YAMLError:
            raise exceptions.ConfigSyntaxError("Error parsing YAML")

        if "printer" in config:
            self._printer_config = config["printer"]
            self._printer_name = self._printer_config.pop("type").title()

            if not self._printer_name or not hasattr(printer, self._printer_name):
                raise exceptions.ConfigSyntaxError(
                    'Printer type "{printer_name}" is invalid'.format(
                        printer_name=self._printer_name,
                    )
                )

        self._has_loaded = True

    def printer(self):
        """Returns a printer that was defined in the config, or throws an
        exception.

        This method loads the default config if one hasn't beeen already loaded.

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
