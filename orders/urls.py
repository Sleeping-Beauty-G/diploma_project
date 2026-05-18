from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CartItemViewSet, CartViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"cart/items", CartItemViewSet, basename="cart-items")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
