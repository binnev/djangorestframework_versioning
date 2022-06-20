from typing import Type, Union, TYPE_CHECKING

from packaging.version import Version as _Version

from drf_versioning.exceptions import VersionDoesNotExist

if TYPE_CHECKING:
    from drf_versioning.transform import Transform


class Version(_Version):
    notes: list[str]
    transforms: list[Type["Transform"]]

    def __init__(
        self,
        version: str,
        notes=None,
        transforms=None,
    ) -> None:
        self.notes = notes or []
        self.transforms = transforms or []
        for transform in self.transforms:
            transform.version = self
        super().__init__(version)

    @classmethod
    def list(cls):
        raise NotImplementedError(
            "You need to subclass this and provide the .list() method which returns a list of "
            "Version instances"
        )

    @classmethod
    def get(cls, version_str: str):
        try:
            return next(v for v in cls.list() if v.base_version == version_str)
        except StopIteration:
            raise VersionDoesNotExist(version_str)

    @classmethod
    def get_latest(cls):
        return max(cls.list())

    def __lt__(self, other: Union[str, "Version"]) -> bool:
        return super().__lt__(parse_other(other))

    def __le__(self, other: Union[str, "Version"]) -> bool:
        return super().__le__(parse_other(other))

    def __eq__(self, other: Union[str, "Version"]) -> bool:
        return super().__eq__(parse_other(other))

    def __ge__(self, other: Union[str, "Version"]) -> bool:
        return super().__ge__(parse_other(other))

    def __gt__(self, other: Union[str, "Version"]) -> bool:
        return super().__gt__(parse_other(other))


def parse_other(other):
    return other if isinstance(other, _Version) else Version(other)
