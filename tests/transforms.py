from drf_versioning.transform import AddField


class ThingTransformAddNumber(AddField):
    field_name = "number"
    description = "Added Thing.number field."
