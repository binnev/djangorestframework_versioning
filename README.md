# Django Rest Framework Versioning
Work In Progress! 

Todo: 
- Add Versions for the versions of this repo :mind-blown:
- BUG: Allow multiple transforms per version -.-
- Have Transform, VersionedViewSet add themselves to Version's .transforms/.views attributes. (The reverse is pretty cumbersome to maintain)
- Version class 
  - Admin page for Versions (no editing, but just to view what is included in each version)
  - Overridable Version class
  - Version class to have methods to describe Transforms, ViewSets / views, etc 
  - FUTURE and PAST version singletons (?) that always "win" comparisons with normal Versions.
    - This will allow marking features with introduced_in=Version.FUTURE, allowing release to be postponed till a later version. 
-VersionedSerializer 
  - Make VersionedSerializer work as inline serializer 
    - Needs to get context.request from parent probably
  - Hard(er) link between VersioningSerializer and its transforms
- Make VersionDoesNotExist a subclass of rest framework APIerror so views can handle it. 
- The holy grail: get drf's openapi schema generator to listen to all this stuff. 
- Startup checks: 
  - VersioningSerializers have transform_base declared
- Cases for the transforms to handle (**add your edge cases here!**) (and examples in the docs): 
  - Field becomes required / nullable or reverse
  - Add value to field choices (shouldn't appear in old schema)
  - Add value to field schema and map to old value. E. G. Active / Failed -> Active /Failed / Retrying but for older versions Retrying should be displayed as Failed

