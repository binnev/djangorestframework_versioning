import pytest
from packaging.version import InvalidVersion

from drf_versioning.exceptions import VersionDoesNotExist
from drf_versioning.version import Version
from tests import versions


def test_version_list_retrieves_from_settings():
    assert Version.list() == versions.VERSIONS


def test_get_happy():
    assert Version.get("2.0.0") == versions.VERSION_2_0_0


@pytest.mark.parametrize(
    "input, expected_exception",
    [
        ("bad_version", InvalidVersion),
        ("666.420.69", VersionDoesNotExist),
    ],
)
def test_get_sad(input, expected_exception):
    with pytest.raises(expected_exception) as e:
        Version.get(input)


@pytest.mark.parametrize(
    "settings_default, expected_version",
    [
        ("2.0.0", versions.VERSION_2_0_0),
        ("earliest", versions.VERSION_1_0_0),
        ("latest", versions.VERSION_2_1_0),
    ],
)
def test_get_default_happy(settings_default, expected_version, patch_settings):
    """The user can specify a specific version as default, or use "earliest" / "latest"."""
    with patch_settings(DEFAULT_VERSION=settings_default):
        assert Version.get_default() == expected_version


@pytest.mark.parametrize(
    "input, expected_exception",
    [
        ("bad_version", InvalidVersion),
        ("666.420.69", VersionDoesNotExist),
    ],
)
def test_get_default_sad(input, expected_exception, patch_settings):
    with patch_settings(DEFAULT_VERSION=input):
        with pytest.raises(expected_exception):
            Version.get_default()
