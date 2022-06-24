from drf_versioning.views import VersionViewSet
from tests.versions import VERSIONS


def test_version_viewset_get_queryset():
    assert VersionViewSet().get_queryset() == VERSIONS
