from rest_framework.routers import DefaultRouter
from .api_views import BidhaaViewSet, SaleViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'bidhaas', BidhaaViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = router.urls
