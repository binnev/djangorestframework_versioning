from unittest.mock import patch

import pytest

from drf_versioning.middleware import GetDefaultMixin
from drf_versioning.version import Version


@pytest.mark.parametrize(
    "super_version, expected_version",
    [
        ("2.0.0", "2.0.0"),  # version passed in request
        (None, "666.69.420"),  # no version in request -> use default
    ],
)
@patch("drf_versioning.version.base.Version.get_default", return_value=Version("666.69.420"))
@patch("rest_framework.versioning.BaseVersioning.determine_version")
def test_accept_header_versioning(
    mock, mock_get_default, super_version, expected_version, patch_settings
):
    mock.return_value = super_version
    version = GetDefaultMixin().determine_version(...)

    assert isinstance(version, str)
    assert version == expected_version
    mock.assert_called_with(...)
