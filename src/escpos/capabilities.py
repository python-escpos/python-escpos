import re
import six
from os import path
import yaml


# Load external printer database
with open(path.join(path.dirname(__file__), 'capabilities.json')) as f:
    CAPABILITIES = yaml.load(f)

PROFILES = CAPABILITIES['profiles']



class NotSupported(Exception):
    pass


BARCODE_B = 'barcodeB'


class BaseProfile(object):
    """This respresents a printer profile.

    A printer profile knows about the number of columns, supported
    features, colors and more.
    """

    profile_data = {}

    def __getattr__(self, name):
        return self.profile_data[name]

    def get_font(self, font):
        """Return the escpos index for `font`. Makes sure that
        the requested `font` is valid.
        """
        font = {'a': 0, 'b': 1}.get(font, font)
        if not six.text_type(font) in self.fonts:
            raise NotSupported(
                '"%s" is not a valid font in the current profile' % font)
        return font

    def get_columns(self, font):
        """ Return the number of columns for the given font.
        """
        font = self.get_font(font)
        return self.fonts[six.text_type(font)]['columns']

    def supports(self, feature):
        """Return true/false for the given feature.
        """
        return self.features.get(feature)

    def get_code_pages(self):
        """Return the support code pages as a {name: index} dict.
        """
        return {v.lower(): k for k, v in self.codePages.items()}



def get_profile(name=None, **kwargs):
    """Get the profile by name; if no name is given, return the
    default profile.
    """
    if isinstance(name, Profile):
        return name

    clazz = get_profile_class(name or 'default')
    return clazz(**kwargs)


CLASS_CACHE = {}


def get_profile_class(name):
    """For the given profile name, load the data from the external
    database, then generate dynamically a class.
    """
    if not name in CLASS_CACHE:
        profile_data = PROFILES[name]
        profile_name = clean(name)
        class_name = '{}{}Profile'.format(
            profile_name[0].upper(), profile_name[1:])
        new_class = type(class_name, (BaseProfile,), {'profile_data': profile_data})
        CLASS_CACHE[name] = new_class

    return CLASS_CACHE[name]


def clean(s):
   # Remove invalid characters
   s = re.sub('[^0-9a-zA-Z_]', '', s)
   # Remove leading characters until we find a letter or underscore
   s = re.sub('^[^a-zA-Z_]+', '', s)
   return str(s)


# For users, who want to provide their profile
class Profile(get_profile_class('default')):

    def __init__(self, columns=None, features=None):
        super(Profile, self).__init__()

        self.columns = columns
        self.features = features or {}

    def get_columns(self, font):
        if self.columns is not None:
            return self.columns

        return super(Profile, self).get_columns(font)




