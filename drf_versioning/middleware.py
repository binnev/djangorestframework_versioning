from rest_framework import versioning

from .version import Version


class GetDefaultMixin(versioning.BaseVersioning):
    """Return a default version instead of None, if no version is passed with the request."""

    def determine_version(self, request, *args, **kwargs):
        version = super().determine_version(request, *args, **kwargs)
        if version is None:
            return Version.get_default().base_version
        return version


class AcceptHeaderVersioning(GetDefaultMixin, versioning.AcceptHeaderVersioning):
    pass


class NamespaceVersioning(GetDefaultMixin, versioning.NamespaceVersioning):
    pass


class URLPathVersioning(GetDefaultMixin, versioning.URLPathVersioning):
    pass


class HostNameVersioning(GetDefaultMixin, versioning.HostNameVersioning):
    pass


class QueryParameterVersioning(GetDefaultMixin, versioning.QueryParameterVersioning):
    pass
