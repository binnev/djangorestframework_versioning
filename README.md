# Django Rest Framework Versioning
Work In Progress! 

Todo: 
- Lazy settings to allow user to specify location of Versions list
- Make VersionedSerializer work as inline serializer 
  - Needs to get context.request from parent probably
- Hard(er) link between VersioningSerializer and its transforms
- decorator to version viewset actions.
- The holy grail: get drf's openapi schema generator to listen to all this stuff. 