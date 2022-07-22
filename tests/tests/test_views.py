import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, APIClient

from drf_versioning.views import VersionViewSet
from tests.models import Thing

pytestmark = pytest.mark.django_db


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


@pytest.mark.parametrize(
    "request_method, url, request_version, expected_status_code",
    [
        ("get", "/thing/", "1.0.0", 404),  # viewset introduced but list action not yet introduced
        ("get", "/thing/", "2.0.0", 200),
        ("get", "/thing/", "2.1.0", 200),
        ("get", "/thing/", "2.2.0", 404),  # viewset removed in v2.2.0
        ("get", "/thing/666/", "1.0.0", 200),
        ("get", "/thing/666/", "2.0.0", 200),
        ("get", "/thing/666/", "2.1.0", 404),  # retrieve action removed in v2.1.0
        ("get", "/thing/666/", "2.2.0", 404),
        ("get", "/thing/666/get_name/", "1.0.0", 404),
        ("get", "/thing/666/get_name/", "2.0.0", 404),
        ("get", "/thing/666/get_name/", "2.1.0", 200),  # get_name introduced in v2.1.0
        ("get", "/thing/666/get_name/", "2.2.0", 404),
        # the rest just obey the viewset introduced_in/removed_in
        ("post", "/thing/", "1.0.0", 201),
        ("post", "/thing/", "2.0.0", 201),
        ("post", "/thing/", "2.1.0", 201),
        ("post", "/thing/", "2.2.0", 404),
        ("delete", "/thing/666/", "1.0.0", 204),
        ("delete", "/thing/666/", "2.0.0", 204),
        ("delete", "/thing/666/", "2.1.0", 204),
        ("delete", "/thing/666/", "2.2.0", 404),
        ("patch", "/thing/666/", "1.0.0", 200),
        ("patch", "/thing/666/", "2.0.0", 200),
        ("patch", "/thing/666/", "2.1.0", 200),
        ("patch", "/thing/666/", "2.2.0", 404),
    ],
)
def test_thing_viewset(request_method, url, request_version, expected_status_code):
    mixer.blend(Thing, id=666)
    client = APIClient()
    body = {"name": "foo", "number": 420}
    method = getattr(client, request_method)
    response = method(
        url, HTTP_ACCEPT=f"application/json; version={request_version}", data=body, format="json"
    )
    assert response.status_code == expected_status_code
