from drf_versioning.settings import versioning_settings
from tests.versions import VERSIONS


def test_settings():
    assert versioning_settings.VERSION_LIST == VERSIONS
