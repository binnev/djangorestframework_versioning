from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("thing", views.ThingViewSet, basename="thing")

urlpatterns = router.urls
