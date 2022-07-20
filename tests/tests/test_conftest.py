from drf_versioning.settings import versioning_settings
from tests.versions import VERSIONS

MOCK_VERSIONS = ["foo", "bar"]


def test_patch_settings(patch_settings):
    with patch_settings(
        DEFAULT_VERSION="6.9.0",
        VERSION_LIST="tests.tests.test_conftest.MOCK_VERSIONS",
    ):
        # settings should be changed inside context manager
        assert versioning_settings.DEFAULT_VERSION == "6.9.0"
        assert versioning_settings.VERSION_LIST == MOCK_VERSIONS

    # settings should be reverted outside context manager
    assert versioning_settings.DEFAULT_VERSION == "latest"
    assert versioning_settings.VERSION_LIST == VERSIONS
