import os
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, ProductInfo
from .serializers import ProductSerializer, ProductInfoSerializer
from .tasks import import_products


class IsSupplierOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(
            request.user, "role", None
        ) in ["supplier", "admin"]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.prefetch_related("product_infos__parameters__parameter")
    serializer_class = ProductSerializer


class ProductInfoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductInfoSerializer
    permission_classes = [IsSupplierOrAdmin]

    def get_queryset(self):
        queryset = ProductInfo.objects.select_related("product", "supplier")
        user = self.request.user

        if getattr(user, "role", None) == "supplier":
            # Показывать только свои ProductInfo
            queryset = queryset.filter(supplier__user=user)

        return queryset

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsSupplierOrAdmin],
    )
    def change_quantity(self, request, pk=None):
        product_info = self.get_object()

        quantity = request.data.get("quantity")

        if quantity is None:
            return Response(
                {"error": "Quantity is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quantity = int(quantity)
        except ValueError:
            return Response(
                {"error": "Quantity must be a number"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 0:
            return Response(
                {"error": "Quantity cannot be negative"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product_info.quantity = quantity
        product_info.save()

        return Response(
            {
                "status": "quantity updated",
                "product_id": product_info.id,
                "quantity": product_info.quantity,
            }
        )

    @action(detail=False, methods=["post"])
    def import_yaml(self, request):
        file_path = request.data.get("file_path")

        if (
            not file_path
            or not os.path.isfile(file_path)
            or not file_path.endswith(".yaml")
        ):
            return Response(
                {"error": "File not found or invalid format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        import_products.delay(file_path)

        return Response({"status": "import started"}, status=status.HTTP_202_ACCEPTED)
