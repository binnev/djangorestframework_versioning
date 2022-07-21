from unittest.mock import MagicMock

import pytest
from django.http import Http404

from drf_versioning.decorators import versioned_view
from drf_versioning.decorators.utils import get_min_version, get_max_version
from drf_versioning.version import Version
from tests import versions


@pytest.mark.parametrize(
    "kwargs, request_version, expected_result",
    [
        (dict(introduced_in=versions.VERSION_2_0_0), versions.VERSION_1_0_0, 404),
        (dict(introduced_in=versions.VERSION_2_0_0), versions.VERSION_2_0_0, 200),
        (dict(introduced_in=versions.VERSION_2_0_0), versions.VERSION_2_1_0, 200),
        (dict(removed_in=versions.VERSION_2_0_0), versions.VERSION_1_0_0, 200),
        (dict(removed_in=versions.VERSION_2_0_0), versions.VERSION_2_0_0, 404),
        (dict(removed_in=versions.VERSION_2_0_0), versions.VERSION_2_1_0, 404),
        (
            dict(introduced_in=versions.VERSION_2_0_0, removed_in=versions.VERSION_2_1_0),
            versions.VERSION_1_0_0,
            404,
        ),
        (
            dict(introduced_in=versions.VERSION_2_0_0, removed_in=versions.VERSION_2_1_0),
            versions.VERSION_2_0_0,
            200,
        ),
        (
            dict(introduced_in=versions.VERSION_2_0_0, removed_in=versions.VERSION_2_1_0),
            versions.VERSION_2_1_0,
            404,
        ),
        (
            dict(introduced_in=versions.VERSION_2_0_0, removed_in=versions.VERSION_2_1_0),
            versions.VERSION_2_2_0,
            404,
        ),
    ],
)
def test_versioned_view(kwargs, request_version, expected_result):
    @versioned_view(**kwargs)
    def mock_view(viewset, request, *args, **kwargs):
        return 200

    request = MagicMock()
    request.version = request_version
    if expected_result == 404:
        with pytest.raises(Http404):
            mock_view(..., request)
    else:
        assert mock_view(..., request) == expected_result


@pytest.mark.parametrize(
    "view_min, viewset_min, expected_result",
    [
        (None, None, versions.VERSION_1_0_0),
        (Version("1.0"), None, Version("1.0")),
        (None, Version("1.0"), Version("1.0")),
        (Version("1.0"), Version("1.0"), Version("1.0")),
        (Version("2.0"), Version("1.0"), Version("2.0")),
        (Version("1.0"), Version("2.0"), Version("2.0")),
    ],
)
def test_get_min_version(view_min, viewset_min, expected_result):
    assert get_min_version(view_min, viewset_min) == expected_result


@pytest.mark.parametrize(
    "view_max, viewset_max, expected_result",
    [
        (None, None, Version.get_latest()),
        (Version("1.0"), None, Version("1.0")),
        (None, Version("1.0"), Version("1.0")),
        (Version("1.0"), Version("1.0"), Version("1.0")),
        (Version("2.0"), Version("1.0"), Version("1.0")),
        (Version("1.0"), Version("2.0"), Version("1.0")),
    ],
)
def test_get_max_version(view_max, viewset_max, expected_result):
    assert get_max_version(view_max, viewset_max) == expected_result
