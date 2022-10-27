from rest_framework import versioning

from .versions import Version


class GetDefaultMixin(versioning.BaseVersioning):
    """
    If no version is passed with the request -> return default version
    If unknown version is passed in the request -> raise VersionDoesNotExist
    """

    def determine_version(self, request, *args, **kwargs):
        version = super().determine_version(request, *args, **kwargs)
        if not version:
            return Version.get_default().base_version
        return Version.get(version).base_version


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
