from rest_framework.versioning import AcceptHeaderVersioning as _AcceptHeaderVersioning

from drf_versioning.version import Version


class AcceptHeaderVersioning(_AcceptHeaderVersioning):
    def determine_version(self, request, *args, **kwargs):
        version = super().determine_version(request, *args, **kwargs)
        version = Version.get(version) if version else Version.get_latest()
        return version
