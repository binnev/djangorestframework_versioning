from contextlib import contextmanager

import pytest
from django.conf import settings
from django.test.utils import override_settings


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
