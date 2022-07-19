from unittest.mock import patch

import pytest
from packaging.version import InvalidVersion

from drf_versioning.version import Version
from tests import versions


def test_version_list_retrieves_from_settings():
    assert Version.list() == versions.VERSIONS


@pytest.mark.parametrize(
    "settings_default, expected_version",
    [
        ("2.0.0", versions.VERSION_2_0_0),
        ("earliest", versions.VERSION_1_0_0),
        ("latest", versions.VERSION_2_1_0),
    ],
)
@patch("drf_versioning.version.base.versioning_settings")
def test_get_default_happy(mock, settings_default, expected_version):
    """The user can specify a specific version as default, or use "earliest" | "latest"."""
    mock.DEFAULT_VERSION = settings_default
    mock.VERSION_LIST = versions.VERSIONS
    assert Version.get_default() == expected_version


@patch("drf_versioning.version.base.versioning_settings")
def test_get_default_sad(mock):
    mock.DEFAULT_VERSION = "bad_version"
    with pytest.raises(InvalidVersion) as e:
        Version.get_default()
    assert str(e.value) == "bad_version"
