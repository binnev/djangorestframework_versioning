from drf_versioning.transform import AddField
from tests import versions

# fixme: the reason this doesn't get registered with v2.1.0 is because nothing imports this file...
class ThingTransformAddNumber(AddField):
    field_name = "number"
    description = "Added Thing.number field."
    version = versions.VERSION_2_1_0
