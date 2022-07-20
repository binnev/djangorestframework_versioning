from rest_framework.test import APIRequestFactory

from drf_versioning.views import VersionViewSet


def test_my_version():
    factory = APIRequestFactory()
    request = factory.get("", HTTP_ACCEPT="application/json; version=2.0.0")
    view = VersionViewSet.as_view(actions={"get": "my_version"})
    response = view(request)
    assert response.status_code == 200
    assert response.data == {
        "version": "2.0.0",
        "notes": ["Added Thing model."],
    }
