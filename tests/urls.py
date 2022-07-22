from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("thing", views.ThingViewSet, basename="thing")
router.register("thing2", views.OtherThingViewSet, basename="thing2")

urlpatterns = router.urls
