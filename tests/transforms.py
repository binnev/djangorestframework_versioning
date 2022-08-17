from drf_versioning.transform import AddField
from tests import versions


class ThingTransformAddNumber(AddField):
    field_name = "number"
    description = "Added Thing.number field."
    version = versions.VERSION_2_1_0
