from drf_versioning.version import Version
from tests.versions import VERSIONS


def test_version_list_retrieves_from_settings():
    assert Version.list() == VERSIONS
