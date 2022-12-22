from drf_versioning.versions import Version as _Version


class Version(_Version):
    """For testing extensibility of Version object."""

    date_created: str

    def __init__(self, version: str, notes=None, date_created: str = "today"):
        super().__init__(version, notes)
        self.date_created = date_created


VERSION_0_0_1 = Version("0.0.1", notes=["Pre-release"])
VERSION_1_0_0 = Version("1.0.0", notes=["Initial version"])
VERSION_2_0_0 = Version("2.0.0", notes=["Added Thing model."])
VERSION_2_1_0 = Version("2.1.0")
VERSION_2_2_0 = Version("2.2.0")
VERSION_2_3_0 = Version("2.3.0")

VERSIONS = (
    VERSION_0_0_1,
    VERSION_1_0_0,
    VERSION_2_0_0,
    VERSION_2_1_0,
    VERSION_2_2_0,
    VERSION_2_3_0,
)
