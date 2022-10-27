import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, APIClient

from drf_versioning.exceptions import VersionsNotDeclaredError
from drf_versioning.versions import Version
from drf_versioning.versions.views import VersionViewSet
from drf_versioning.views import VersionedViewSet
from tests.models import Thing

pytestmark = pytest.mark.django_db


def test_my_version():
    factory = APIRequestFactory()
    request = factory.get("", HTTP_ACCEPT="application/json; version=2.0.0")
    view = VersionViewSet.as_view(actions={"get": "my_version"})
    response = view(request)
    assert response.status_code == 200
    assert response.data["version"] == "2.0.0"


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


@pytest.mark.parametrize(
    "request_method, url, request_version, expected_status_code",
    [
        ("get", "/thing2/", "1.0.0", 404),  # viewset introduced but list action not yet introduced
        ("get", "/thing2/", "2.0.0", 200),
        ("get", "/thing2/", "2.1.0", 200),
        ("get", "/thing2/", "2.2.0", 200),
        ("get", "/thing2/666/", "1.0.0", 200),
        ("get", "/thing2/666/", "2.0.0", 200),
        ("get", "/thing2/666/", "2.1.0", 404),  # retrieve action removed in v2.1.0
        ("get", "/thing2/666/", "2.2.0", 404),
        ("get", "/thing2/666/get_name/", "1.0.0", 404),
        ("get", "/thing2/666/get_name/", "2.0.0", 404),
        ("get", "/thing2/666/get_name/", "2.1.0", 200),  # get_name introduced in v2.1.0
        ("get", "/thing2/666/get_name/", "2.2.0", 200),
        # the rest just obey the viewset introduced_in/removed_in
        ("post", "/thing2/", "1.0.0", 201),
        ("post", "/thing2/", "2.0.0", 201),
        ("post", "/thing2/", "2.1.0", 201),
        ("post", "/thing2/", "2.2.0", 201),
        ("delete", "/thing2/666/", "1.0.0", 204),
        ("delete", "/thing2/666/", "2.0.0", 204),
        ("delete", "/thing2/666/", "2.1.0", 204),
        ("delete", "/thing2/666/", "2.2.0", 204),
        ("patch", "/thing2/666/", "1.0.0", 200),
        ("patch", "/thing2/666/", "2.0.0", 200),
        ("patch", "/thing2/666/", "2.1.0", 200),
        ("patch", "/thing2/666/", "2.2.0", 200),
    ],
)
def test_thing2_viewset(request_method, url, request_version, expected_status_code):
    mixer.blend(Thing, id=666)
    client = APIClient()
    body = {"name": "foo", "number": 420}
    method = getattr(client, request_method)
    response = method(
        url, HTTP_ACCEPT=f"application/json; version={request_version}", data=body, format="json"
    )
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "request_method, url, request_version, expected_status_code",
    [
        ("get", "/thing3/", "1.0.0", 404),  # viewset introduced but list action not yet introduced
        ("get", "/thing3/", "2.0.0", 200),
        ("get", "/thing3/", "2.1.0", 200),
        ("get", "/thing3/", "2.2.0", 404),
        ("get", "/thing3/666/", "1.0.0", 200),
        ("get", "/thing3/666/", "2.0.0", 200),
        ("get", "/thing3/666/", "2.1.0", 404),  # retrieve action removed in v2.1.0
        ("get", "/thing3/666/", "2.2.0", 404),
        ("get", "/thing3/666/get_name/", "1.0.0", 404),
        ("get", "/thing3/666/get_name/", "2.0.0", 404),
        ("get", "/thing3/666/get_name/", "2.1.0", 200),  # get_name introduced in v2.1.0
        ("get", "/thing3/666/get_name/", "2.2.0", 404),
        # the rest just obey the viewset introduced_in/removed_in
        ("post", "/thing3/", "1.0.0", 201),
        ("post", "/thing3/", "2.0.0", 201),
        ("post", "/thing3/", "2.1.0", 201),
        ("post", "/thing3/", "2.2.0", 404),
        ("delete", "/thing3/666/", "1.0.0", 204),
        ("delete", "/thing3/666/", "2.0.0", 204),
        ("delete", "/thing3/666/", "2.1.0", 204),
        ("delete", "/thing3/666/", "2.2.0", 404),
        ("patch", "/thing3/666/", "1.0.0", 200),
        ("patch", "/thing3/666/", "2.0.0", 200),
        ("patch", "/thing3/666/", "2.1.0", 200),
        ("patch", "/thing3/666/", "2.2.0", 404),
    ],
)
def test_thing3_viewset(request_method, url, request_version, expected_status_code):
    mixer.blend(Thing, id=666)
    client = APIClient()
    body = {"name": "foo", "number": 420}
    method = getattr(client, request_method)
    response = method(
        url, HTTP_ACCEPT=f"application/json; version={request_version}", data=body, format="json"
    )
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "request_method, url, request_version, expected_status_code",
    [
        # viewset is not versioned, so by default its methods should be available for all versions
        ("get", "/thing4/", "1.0.0", 200),
        ("get", "/thing4/", "2.0.0", 200),
        ("get", "/thing4/", "2.1.0", 200),
        ("get", "/thing4/", "2.2.0", 200),
        ("get", "/thing4/666/", "1.0.0", 404),  # retrieve method not introduced yet
        ("get", "/thing4/666/", "2.0.0", 200),
        ("get", "/thing4/666/", "2.1.0", 200),
        ("get", "/thing4/666/", "2.2.0", 404),  # retrieve method removed in this version
    ],
)
def test_unversioned_thing_viewset(request_method, url, request_version, expected_status_code):
    mixer.blend(Thing, id=666)
    client = APIClient()
    body = {"name": "foo", "number": 420}
    method = getattr(client, request_method)
    response = method(
        url, HTTP_ACCEPT=f"application/json; version={request_version}", data=body, format="json"
    )
    assert response.status_code == expected_status_code


def test_versioned_viewset_meta():
    v420 = Version("4.20")
    v69 = Version("6.9")

    class TestViewSet(VersionedViewSet):
        introduced_in = v420
        removed_in = v69

    assert v420.viewsets_introduced == [TestViewSet]
    assert v420.viewsets_removed == []
    assert v69.viewsets_introduced == []
    assert v69.viewsets_removed == [TestViewSet]


def test_versioned_viewset_meta_enforces_versions():
    with pytest.raises(VersionsNotDeclaredError):

        class BadViewSet(VersionedViewSet):
            pass  # introduced_in and removed_in not declared

    with pytest.raises(VersionsNotDeclaredError):

        class BadViewSet2(VersionedViewSet):
            introduced_in = None
            removed_in = None
