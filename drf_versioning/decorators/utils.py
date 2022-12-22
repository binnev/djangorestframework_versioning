from typing import Optional

from drf_versioning.settings import versioning_settings

Version = versioning_settings.VERSION_MODEL


def get_min_version(view_min: Optional[Version], viewset_min: Optional[Version]):
    if view_min is viewset_min is None:
        return None
    default = Version.get_earliest()
    return max(default, view_min or default, viewset_min or default)


def get_max_version(view_max: Optional[Version], viewset_max: Optional[Version]):
    if view_max is viewset_max is None:
        return None
    default = Version.get_latest()
    return min(default, view_max or default, viewset_max or default)
