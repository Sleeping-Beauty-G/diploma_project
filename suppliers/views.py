from rest_framework import permissions, viewsets

from .models import Supplier
from .serializers import SupplierSerializer


class IsAdminOrSupplier(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(
            request.user, "role", None
        ) in ["admin", "supplier"]

    def has_object_permission(self, request, view, obj):

        if getattr(request.user, "role", None) == "admin":
            return True

        return obj.user == request.user


class SupplierViewSet(viewsets.ModelViewSet):

    serializer_class = SupplierSerializer
    permission_classes = [IsAdminOrSupplier]

    def get_queryset(self):

        user = self.request.user

        queryset = Supplier.objects.select_related("user")

        if getattr(user, "role", None) == "supplier":
            queryset = queryset.filter(user=user)

        return queryset
