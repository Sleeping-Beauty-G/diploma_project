from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ProductInfo
from .serializers import ProductInfoSerializer
from .tasks import import_products


class IsSupplierOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(
            request.user, "role", None
        ) in ["supplier", "admin"]


class AdminProductInfoViewSet(viewsets.ModelViewSet):
    queryset = ProductInfo.objects.select_related("product", "supplier")
    serializer_class = ProductInfoSerializer
    permission_classes = [IsSupplierOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()

        supplier_id = self.request.query_params.get("supplier_id")
        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)

        return queryset

    @action(detail=True, methods=["patch"])
    def change_quantity(self, request, pk=None):
        obj = self.get_object()
        quantity = request.data.get("quantity")

        if quantity is None:
            return Response({"error": "quantity required"}, status=400)

        try:
            quantity = int(quantity)
            if quantity < 0:
                return Response({"error": "quantity cannot be negative"}, status=400)
        except ValueError:
            return Response({"error": "quantity must be integer"}, status=400)

        obj.quantity = quantity
        obj.save()

        return Response({"status": "updated", "quantity": obj.quantity})

    @action(detail=False, methods=["post"])
    def import_yaml(self, request):
        file_path = request.data.get("file_path")

        if not file_path:
            return Response({"error": "file_path required"}, status=400)

        import_products.delay(file_path)

        return Response({"status": "import started"})
