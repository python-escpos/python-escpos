import re
from os import path
import yaml


with open(path.join(path.dirname(__file__), 'capabilities.yml')) as f:
    PROFILES = yaml.load(f)


class Profile(object):

    profile_data = {}

    def __init__(self, columns=None):
        self.default_columns = columns

    def __getattr__(self, name):
        return self.profile_data[name]

    def get_columns(self, font):
        """ Return the number of columns for the given font.
        """
        if self.default_columns:
            return self.default_columns

        if 'columnConfigs' in self.profile_data:
            columns_def = self.columnConfigs[self.defaultColumnConfig]

        elif 'columns' in self.profile_data:
            columns_def = self.columns

        if isinstance(columns_def, int):
            return columns_def
        return columns_def[font]


def get_profile(name=None, **kwargs):
    if isinstance(name, Profile):
        return name

    clazz = get_profile_class(name or 'default')
    return clazz(**kwargs)



CLASS_CACHE = {}


def get_profile_class(name):
    if not name in CLASS_CACHE:
        profile_data = resolve_profile_data(name)
        class_name = '%sProfile' % clean(name)
        new_class = type(class_name, (Profile,), {'profile_data': profile_data})
        CLASS_CACHE[name] = new_class

    return CLASS_CACHE[name]


def clean(s):
   # Remove invalid characters
   s = re.sub('[^0-9a-zA-Z_]', '', s)
   # Remove leading characters until we find a letter or underscore
   s = re.sub('^[^a-zA-Z_]+', '', s)
   return str(s)


def resolve_profile_data(name):
    data = PROFILES[name]
    inherits = data.get('inherits')
    if not inherits:
        return data

    if not isinstance(inherits, (tuple, list)):
        inherits = [inherits]

    merged = {}
    for base in reversed(inherits):
        base_data = resolve_profile_data(base)
        merged.update(base_data)
    merged.update(data)
    return merged


