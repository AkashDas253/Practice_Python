from rest_framework.routers import DefaultRouter
from .api_views import LinkViewSet

router = DefaultRouter()
router.register(r'vault', LinkViewSet, basename='link-vault')

urlpatterns = router.urls