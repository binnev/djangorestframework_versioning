from contextlib import contextmanager

import pytest
from dateutil import tz
from django.conf import settings
from django.test.utils import override_settings
from django.utils import timezone


@pytest.fixture
def patch_settings():
    """Thin wrapper around django's override_settings which allows us to override just some of
    the elements of the settings, without having to provide all the unchanged elements."""
    original_settings = settings.DRF_VERSIONING_SETTINGS

    @contextmanager
    def _patch_settings(**kwargs):
        modified_settings = {**original_settings, **kwargs}
        with override_settings(DRF_VERSIONING_SETTINGS=modified_settings):
            yield

    return _patch_settings


@pytest.fixture(autouse=True)
def stop___hammertime(request, monkeypatch):
    """
    decorate your test with @pytest.mark.cant_touch_this if you want to disable this fixture
    """
    if "cant_touch_this" in request.keywords:
        return

    def earlier():
        return timezone.datetime(2010, 1, 2, 3, 4, 5, tzinfo=tz.UTC)

    monkeypatch.setattr(timezone, "now", earlier)
