from unittest.mock import MagicMock

import pytest
from django.http import Http404

from drf_versioning.decorators import versioned_view
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
