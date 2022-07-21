from drf_versioning.version import Version
from . import transforms

VERSION_1_0_0 = Version("1.0.0", notes=["Initial version"])
VERSION_2_0_0 = Version("2.0.0", notes=["Added Thing model."])
VERSION_2_1_0 = Version("2.1.0", transforms=[transforms.ThingTransformAddNumber])
VERSION_2_2_0 = Version("2.2.0", notes=["Did nothing."])

VERSIONS = (
    VERSION_1_0_0,
    VERSION_2_0_0,
    VERSION_2_1_0,
    VERSION_2_2_0,
)
