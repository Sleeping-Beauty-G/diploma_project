from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .admin_views import AdminProductInfoViewSet
from .views import ProductInfoViewSet, ProductViewSet

router = DefaultRouter()


router.register(r"products", ProductViewSet, basename="products")

router.register(r"product-info", ProductInfoViewSet, basename="product-info")


router.register(
    r"admin/product-info", AdminProductInfoViewSet, basename="admin-product-info"
)

urlpatterns = [
    path("", include(router.urls)),
]
