"""
URL configuration for retail_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from orders.views import CartItemViewSet, OrderViewSet
from products.admin_views import AdminProductInfoViewSet
from products.views import ProductInfoViewSet, ProductViewSet
from suppliers.views import SupplierViewSet
from users.views import AddressViewSet, RegisterView


# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Retail System API",
        default_version="v1",
        description="Diploma project API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()

# Products
router.register(r"products", ProductViewSet, basename="products")
router.register(r"product-info", ProductInfoViewSet, basename="product-info")

# Admin
router.register(
    r"admin/product-info", AdminProductInfoViewSet, basename="admin-product-info"
)

# Orders
router.register(r"cart/items", CartItemViewSet, basename="cart-items")
router.register(r"orders", OrderViewSet, basename="orders")

# Users
router.register(r"addresses", AddressViewSet, basename="addresses")

# Suppliers
router.register(r"suppliers", SupplierViewSet, basename="suppliers")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # Auth
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Swagger
    re_path(
        r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"
    ),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
    # DRF login
    path("api-auth/", include("rest_framework.urls")),
]
