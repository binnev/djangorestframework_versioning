# Django Rest Framework Versioning
Work In Progress! 

Todo: 
- Make VersionedSerializer work as inline serializer 
  - Needs to get context.request from parent probably
- Hard(er) link between VersioningSerializer and its transforms
- Remove custom middleware and make VersioningSerializer do Version.get() instead. 
- Make VersionDoesNotExist a subclass of rest framework APIerror so views can handle it. 
- decorator to version viewset actions.
- The holy grail: get drf's openapi schema generator to listen to all this stuff. 