from rest_framework.versioning import AcceptHeaderVersioning as _AcceptHeaderVersioning

from drf_versioning.version import Version


class AcceptHeaderVersioning(_AcceptHeaderVersioning):
    def determine_version(self, request, *args, **kwargs):
        version = super().determine_version(request, *args, **kwargs)
        if version is None:
            return Version.get_default().base_version
        return version
