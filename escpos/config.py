from __future__ import absolute_import

import os
import appdirs
import yaml

from . import printer
from . import exceptions

class Config(object):

    _app_name = 'python-escpos'
    _config_file = 'config.yaml'

    def __init__(self):
        self._has_loaded = False
        self._printer = None

        self._printer_name = None
        self._printer_config = None

    def load(self, config_path=None):
        if not config_path:
            config_path = os.path.join(
                appdirs.user_config_dir(self._app_name),
                self._config_file
            )

        try:
            with open(config_path) as f:
                config = yaml.load(f)
        except EnvironmentError as e:
            raise exceptions.ConfigNotFoundError('Couldn\'t read config at one or more of {config_path}'.format(
                config_path="\n".join(config_path),
            ))
        except yaml.ParserError as e:
            raise exceptions.ConfigSyntaxError('Error parsing YAML')

        if 'printer' in config:
            self._printer_config = config['printer']
            self._printer_name = self._printer_config.pop('type').title()

            if not self._printer_name or not hasattr(printer, self._printer_name):
                raise exceptions.ConfigSyntaxError('Printer type "{printer_name}" is invalid'.format(
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

