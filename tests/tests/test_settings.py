from drf_versioning import settings
from tests.versions import VERSIONS


def test_settings():
    s = settings.VersioningSettings(
        user_settings={"DEFAULT_VERSION": "6.9"},
        defaults=settings.DEFAULTS,
        import_strings=settings.IMPORT_STRINGS,
    )
    assert s.DEFAULT_VERSION == "6.9"
    assert s.VERSION_LIST == []


def test_settings_loads_version_list():
    assert settings.versioning_settings.VERSION_LIST == VERSIONS
