from typing import Type, Union, TYPE_CHECKING

from packaging.version import Version as _Version, InvalidVersion

from ..exceptions import VersionDoesNotExist
from ..settings import versioning_settings

if TYPE_CHECKING:
    from ..transforms import Transform


class Version(_Version):
    notes: list[str]
    transforms: list[Type["Transform"]]
    viewsets_introduced: list
    viewsets_removed: list
    view_methods_introduced: list
    view_methods_removed: list

    def __init__(
        self,
        version: str,
        notes=None,
    ) -> None:
        self.notes = notes or []
        self.transforms = []
        self.viewsets_introduced = []
        self.viewsets_removed = []
        self.view_methods_introduced = []
        self.view_methods_removed = []
        super().__init__(version)

    @classmethod
    def list(cls):
        return versioning_settings.VERSION_LIST

    @classmethod
    def get(cls, version_str: str):
        try:
            return next(v for v in cls.list() if v == version_str)
        except StopIteration:
            raise VersionDoesNotExist(version_str)

    @classmethod
    def get_latest(cls):
        return max(cls.list())

    @classmethod
    def get_earliest(cls):
        return min(cls.list())

    @classmethod
    def get_default(cls):
        methods = {
            "earliest": cls.get_earliest,
            "latest": cls.get_latest,
        }
        default_version = versioning_settings.DEFAULT_VERSION
        try:
            return Version.get(default_version)
        except InvalidVersion as e:
            try:
                return methods[default_version]()
            except KeyError:
                raise e

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
    if isinstance(other, _Version):
        return other
    elif isinstance(other, str):
        return Version(other)
    else:
        raise InvalidVersion(str(other))
