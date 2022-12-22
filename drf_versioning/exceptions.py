from rest_framework import status
from rest_framework.exceptions import APIException


class VersionDoesNotExist(APIException):
    def __init__(self, version_str: str):
        message = f"Version does not exist: {version_str}"
        super().__init__(message)

    status_code = status.HTTP_406_NOT_ACCEPTABLE


class TransformsNotDeclaredError(Exception):
    pass


class VersionsNotDeclaredError(ValueError):
    def __init__(self, obj_name: str) -> None:
        msg = f"You need to declare either introduced_in or removed_in for {obj_name}"
        super().__init__(msg)
