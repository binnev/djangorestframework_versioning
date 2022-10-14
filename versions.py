"""Using Versions to describe the changes in this versioning library -- wow so meta."""
from drf_versioning.version import Version

VERSION_1_0_0 = Version(
    notes=[
        (
            "VersionedViewSetMeta now checks that all VersionedViewSet subclasses have defined "
            "introduced_in and/or removed_in."
        ),
        "Renamed VersioningSerializer to VersionedSerializer.",
        "VersionedSerializer now supports multiple transforms per version.",
        (
            "VersionedSerializer must now import their list of Transforms and attach it to the "
            "class definition "
        ),
        "Added dateutil as a requirement.",
        "VersionedSerializer can now be used inline.",
    ]
)
VERSION_0_2_0 = Version(
    notes=[
        "Added a list of Versions to track changes to this library.",
        (
            "The link between Version instances and Transform/VersionedViewSet is now defined on "
            "the Transform/VersionedViewSet subclass, and not in the versions list. It makes more "
            "sense to do it this way round because we are passing the Version instance at the "
            "class creation anyway."
        ),
        (
            "On VersionedSerializer subclasses, we now import the Transforms directly using "
            "import_transforms. This has several benefits: 1) Transforms are imported at the "
            "serializer class definition rather than when the Serializer's to_representation is "
            "triggered for the first time. This ensures that the Transform's metaclass (which "
            "adds the Transform to the Version.transforms list) is triggered at startup, "
            "not during first serialization. 2) The Transforms are imported _once_ at class "
            "definition, not every time serialization is performed, so we get a performance "
            "improvement there. "
        ),
        (
            "VersionedSerializer.__init__ checks that transforms have been imported. This means "
            "if they haven't, you'll get the error at startup, not during first serialization."
        ),
    ]
)
VERSION_0_1_1 = Version(
    notes=[
        (
            "Added VersionedViewSet class and versioned_view decorator to allow versioning views. "
            "If the request.version is outside the bounds specified in the ViewSet/method's "
            "`introduced_in` and `removed_in` parameters, a 404 Not Found is returned as if the "
            "view doesn't exist. "
        ),
    ]
)
VERSION_0_1_11 = Version(
    notes=[
        (
            "First semi-usable version of this library. Not worth documenting versions earlier "
            "than this as they were changing so fast and erratically."
        ),
    ]
)
