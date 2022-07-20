# Django Rest Framework Versioning
Work In Progress! 

Todo: 
- Make VersionedSerializer work as inline serializer 
  - Needs to get context.request from parent probably
- Hard(er) link between VersioningSerializer and its transforms
- Make VersionDoesNotExist a subclass of rest framework APIerror so views can handle it. 
- decorator to version viewset actions.
- The holy grail: get drf's openapi schema generator to listen to all this stuff. 
- Startup checks: 
  - VersioningSerializers have transform_base declared
- Field becomes required / nullable or reverse
- Add value to field choices (shouldn't appear in old schema)
- Add value to field schema and map to old value. E. G. Active / Failed -> Active /Failed / Retrying but for older versions Retrying should be displayed as Failed

