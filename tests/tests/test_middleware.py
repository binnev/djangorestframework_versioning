from unittest.mock import patch

import pytest

from drf_versioning.exceptions import VersionDoesNotExist
from drf_versioning.middleware import GetDefaultMixin
from drf_versioning.versions import Version


VERSION_FUTURE = Version("999")
MOCK_VERSION_LIST = [
    Version("4.2.0"),
    Version("6.9"),
]


@pytest.mark.parametrize(
    "super_version, expected_version",
    [
        ("999", "999"),  # version passed in request matches version not in list
        ("6.9", "6.9"),  # version passed in request matches public version in list
        ("666.420", "666.420"),  # completely fictitious version
        (None, "4.2.0"),  # no version in request -> use default
        ("", "4.2.0"),  # no version in request -> use default
    ],
)
@patch("rest_framework.versioning.BaseVersioning.determine_version")
def test_get_default_mixin(mock, super_version, expected_version, patch_settings):
    mock.return_value = super_version
    with patch_settings(
        VERSION_LIST="tests.tests.test_middleware.MOCK_VERSION_LIST",
        DEFAULT_VERSION="earliest",
    ):
        version = GetDefaultMixin().determine_version(...)

    assert isinstance(version, str)
    assert version == expected_version
    mock.assert_called_with(...)
