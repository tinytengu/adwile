from rest_framework.routers import DefaultRouter

from .views import TeaserViewSet

router = DefaultRouter()
router.register("", TeaserViewSet, basename="teaser")

urlpatterns = router.urls
