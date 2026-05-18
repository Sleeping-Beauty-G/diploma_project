from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, RegisterView

router = DefaultRouter()

router.register(r"addresses", AddressViewSet, basename="addresses")

urlpatterns = [
    path("register/", RegisterView.as_view()),
]

urlpatterns += router.urls
