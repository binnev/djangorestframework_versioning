from drf_versioning.transform import AddField
from tests import versions


class ThingTransformAddNumber(AddField):
    field_name = "number"
    description = "Added Thing.number field."
    version = versions.VERSION_2_1_0


class ThingAddStatus(AddField):
    field_name = "status"
    description = "Added Thing.status field"
    version = versions.VERSION_2_2_0


class ThingAddDateUpdated(AddField):
    field_name = "date_updated"
    description = "Added Thing.date_updated field"
    version = versions.VERSION_2_2_0


class PersonAddBirthday(AddField):
    field_name = "birthday"
    description = "Added Person.birthday"
    version = versions.VERSION_2_3_0
