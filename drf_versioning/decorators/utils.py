from typing import Optional

from drf_versioning.version import Version


def get_min_version(view_min: Optional[Version], viewset_min: Optional[Version]):
    default = Version.get_earliest()
    return max(default, view_min or default, viewset_min or default)


def get_max_version(view_max: Optional[Version], viewset_max: Optional[Version]):
    default = Version.get_latest()
    return min(default, view_max or default, viewset_max or default)
