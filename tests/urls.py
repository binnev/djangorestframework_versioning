from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("thing", views.ThingViewSet, basename="thing")
router.register("thing2", views.OtherThingViewSet, basename="thing2")
router.register("thing3", views.YetAnotherThingViewSet, basename="thing3")
router.register("thing4", views.UnversionedThingViewSet, basename="thing4")

urlpatterns = router.urls
