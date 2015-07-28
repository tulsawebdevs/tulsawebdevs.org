from rest_framework.routers import DefaultRouter

from api.views import LocationViewSet


router = DefaultRouter()

router.register(r'locations', LocationViewSet, base_name='location')


urlpatterns = router.urls
