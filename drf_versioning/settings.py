"""
Inspired by (shamelessly pinched from) rest_framework.settings :)
"""

from django.conf import settings
from django.test.signals import setting_changed
from rest_framework.settings import perform_import

DEFAULTS = {
    ...,
}

IMPORT_STRINGS = [
    ...,
]

REMOVED_SETTINGS = []


class VersioningSettings:
    """
    Clone of rest_framework.settings.APISettings
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "DRF_VERSIONING_SETTINGS", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid versioning setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "https://www.django-rest-framework.org/api-guide/settings/"  # fixme
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    "The '%s' setting has been removed. Please refer to '%s' for available settings."
                    % (setting, SETTINGS_DOC)
                )
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


versioning_settings = VersioningSettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_versioning_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "DRF_VERSIONING_SETTINGS":
        versioning_settings.reload()


setting_changed.connect(reload_versioning_settings())