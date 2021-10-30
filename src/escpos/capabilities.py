import re
from os import environ, path
import pkg_resources
import pickle
import logging
import time

import six
import yaml

from tempfile import gettempdir
import platform

from typing import Any, Dict

logging.basicConfig()
logger = logging.getLogger(__name__)

pickle_dir = environ.get("ESCPOS_CAPABILITIES_PICKLE_DIR", gettempdir())
pickle_path = path.join(
    pickle_dir, "{v}.capabilities.pickle".format(v=platform.python_version())
)
# get a temporary file from pkg_resources if no file is specified in env
capabilities_path = environ.get(
    "ESCPOS_CAPABILITIES_FILE",
    pkg_resources.resource_filename(__name__, "capabilities.json"),
)

# Load external printer database
t0 = time.time()
logger.debug("Using capabilities from file: %s", capabilities_path)
if path.exists(pickle_path):
    if path.getmtime(capabilities_path) > path.getmtime(pickle_path):
        logger.debug("Found a more recent capabilities file")
        full_load = True
    else:
        full_load = False
        logger.debug("Loading capabilities from pickle in %s", pickle_path)
        with open(pickle_path, "rb") as cf:
            CAPABILITIES = pickle.load(cf)
else:
    logger.debug("Capabilities pickle file not found: %s", pickle_path)
    full_load = True

if full_load:
    logger.debug("Loading and pickling capabilities")
    with open(capabilities_path) as cp, open(pickle_path, "wb") as pp:
        CAPABILITIES = yaml.safe_load(cp)
        pickle.dump(CAPABILITIES, pp, protocol=2)

logger.debug("Finished loading capabilities took %.2fs", time.time() - t0)


PROFILES: Dict[str, Any] = CAPABILITIES["profiles"]


class NotSupported(Exception):
    """Raised if a requested feature is not supported by the
    printer profile.
    """

    pass


BARCODE_B = "barcodeB"


class BaseProfile(object):
    """This represents a printer profile.

    A printer profile knows about the number of columns, supported
    features, colors and more.
    """

    profile_data: Dict[str, Any] = {}

    def __getattr__(self, name):
        return self.profile_data[name]

    def get_font(self, font) -> int:
        """Return the escpos index for `font`. Makes sure that
        the requested `font` is valid.
        """
        font = {"a": 0, "b": 1}.get(font, font)
        if not six.text_type(font) in self.fonts:
            raise NotSupported(
                '"{}" is not a valid font in the current profile'.format(font)
            )
        return font

    def get_columns(self, font):
        """Return the number of columns for the given font."""
        font = self.get_font(font)
        return self.fonts[six.text_type(font)]["columns"]

    def supports(self, feature):
        """Return true/false for the given feature."""
        return self.features.get(feature)

    def get_code_pages(self):
        """Return the support code pages as a ``{name: index}`` dict."""
        return {v: k for k, v in self.codePages.items()}


def get_profile(name: str = None, **kwargs):
    """Get the profile by name; if no name is given, return the
    default profile.
    """
    if isinstance(name, Profile):
        return name

    clazz = get_profile_class(name or "default")
    return clazz(**kwargs)


CLASS_CACHE = {}


def get_profile_class(name: str):
    """For the given profile name, load the data from the external
    database, then generate dynamically a class.
    """
    if name not in CLASS_CACHE:
        profile_data = PROFILES[name]
        profile_name = clean(name)
        class_name = "{}{}Profile".format(profile_name[0].upper(), profile_name[1:])
        new_class = type(class_name, (BaseProfile,), {"profile_data": profile_data})
        CLASS_CACHE[name] = new_class

    return CLASS_CACHE[name]


def clean(s):
    # Remove invalid characters
    s = re.sub("[^0-9a-zA-Z_]", "", s)
    # Remove leading characters until we find a letter or underscore
    s = re.sub("^[^a-zA-Z_]+", "", s)
    return str(s)


class Profile(get_profile_class("default")):
    """
    For users, who want to provide their profile
    """

    def __init__(self, columns=None, features=None):
        super(Profile, self).__init__()

        self.columns = columns
        self.features = features or {}

    def get_columns(self, font):
        if self.columns is not None:
            return self.columns

        return super(Profile, self).get_columns(font)
