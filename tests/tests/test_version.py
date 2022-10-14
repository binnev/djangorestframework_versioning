import operator
from unittest.mock import patch

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
        ("2.0.0", Version("2.0")),
        ("earliest", Version("1.0")),
        ("latest", Version("3.0")),
    ],
)
@patch("drf_versioning.version.base.Version.list")
def test_get_default_happy(mock, settings_default, expected_version, patch_settings):
    """The user can specify a specific version as default, or use "earliest" / "latest"."""
    mock.return_value = [
        Version("1.0"),
        Version("2.0"),
        Version("3.0"),
    ]
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


@pytest.mark.parametrize(
    "v_left, v_right, op, expected_output",
    [
        ("1.0", "2.0", operator.lt, True),
        ("1.0", "2.1", operator.le, True),
        ("1.0", "2.2", operator.gt, False),
        ("1.0", "2.3", operator.ge, False),
        ("1.0", "2.4", operator.eq, False),
        ("1.0", "1.0", operator.eq, True),
    ],
)
def test_comparison_happy(v_left, v_right, op, expected_output):
    # comparison between Version instances
    assert op(Version(v_left), Version(v_right)) == expected_output

    # if one is a string, it should also work
    assert op(Version(v_left), v_right) == expected_output
    assert op(v_left, Version(v_right)) == expected_output
