from typing import Type, Union, TYPE_CHECKING

from packaging.version import Version as _Version, InvalidVersion

from drf_versioning.settings import versioning_settings

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
        return versioning_settings.VERSION_LIST

    @classmethod
    def get(cls, version_str: str):
        try:
            return next(v for v in cls.list() if v.base_version == version_str)
        except StopIteration:
            raise InvalidVersion(version_str)

    @classmethod
    def get_latest(cls):
        return max(cls.list())

    @classmethod
    def get_earliest(cls):
        return min(cls.list())

    @classmethod
    def get_default(cls):
        mapping = {
            "earliest": cls.get_earliest,
            "latest": cls.get_latest,
        }
        default_version = versioning_settings.DEFAULT_VERSION
        try:
            return Version(default_version)
        except InvalidVersion:
            try:
                return mapping[default_version]()
            except KeyError:
                raise InvalidVersion(default_version)
        if default_version in mapping:
            return mapping[default_version]()
        else:
            return default_version

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
