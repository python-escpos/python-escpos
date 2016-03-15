from __future__ import absolute_import

import os
import appdirs
from localconfig import config

from . import printer
from .exceptions import *

class Config(object):

    _app_name = 'python-escpos'
    _config_file = 'config.ini'

    def __init__(self):
        self._has_loaded = False
        self._printer = None

        self._printer_name = None
        self._printer_config = None

    def load(self, config_path=None):
        # If they didn't pass one, load default
        if not config_path:
            config_path = os.path.join(
                appdirs.user_config_dir(self._app_name),
                self._config_file
            )

        # Deal with one config or a list of them
        # Configparser does this, but I need it for the list in the error message
        if isinstance(config_path, basestring):
            config_path = [config_path]

        files_read = config.read(config_path)
        if not files_read:
            raise ConfigNotFoundError('Couldn\'t read config at one or more of {config_path}'.format(
                config_path="\n".join(config_path),
            ))

        if 'printer' in config:
            # For some reason, dict(config.printer) raises
            # TypeError: attribute of type 'NoneType' is not callable
            self._printer_config = dict(list(config.printer))
            self._printer_name = self._printer_config.pop('type').title()

            if not self._printer_name or not hasattr(printer, self._printer_name):
                raise ConfigSyntaxError('Printer type "{printer_name}" is invalid'.format(
                    printer_name=self._printer_name,
                ))

        self._has_loaded = True

    def printer(self):
        if not self._has_loaded:
            self.load()

        if not self._printer:
            # We could catch init errors and make them a ConfigSyntaxError, 
            # but I'll just let them pass
            self._printer = getattr(printer, self._printer_name)(**self._printer_config)

        return self._printer

