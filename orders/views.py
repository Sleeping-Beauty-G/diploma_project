from django.db import transaction

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import ProductInfo
from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartItemSerializer,
    CartSerializer,
    OrderSerializer,
)
from .tasks import send_order_email_task
from .services.order_service import OrderService


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "client"
        )


class IsAdminOrSupplier(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(
            request.user, "role", None
        ) in ["admin", "supplier"]


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CartItem.objects.none()

        return CartItem.objects.filter(cart__user=self.request.user).select_related(
            "product"
        )

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Cart.objects.none()

        return Cart.objects.filter(user=self.request.user).prefetch_related(
            "items__product"
        )


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Order.objects.none()

        return Order.objects.filter(user=self.request.user).prefetch_related("items")

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        user = request.user
        address = request.data.get("address")

        if not address:
            return Response(
                {"error": "Address required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = Cart.objects.prefetch_related("items__product").filter(user=user).first()

        if not cart or not cart.items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():

            order = OrderService.create_order(user, cart, address)

            for item in cart.items.all():

                product_info = (
                    ProductInfo.objects.select_for_update()
                    .select_related("supplier")
                    .filter(
                        product=item.product,
                        quantity__gte=item.quantity,
                    )
                    .first()
                )

                if not product_info:
                    return Response(
                        {"error": (f"Not enough stock " f"for {item.product.name}")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                product_info.quantity -= item.quantity
                product_info.save()

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    supplier=product_info.supplier,
                    quantity=item.quantity,
                    price=product_info.price,
                )

            cart.items.all().delete()

        send_order_email_task.delay(user.email, order.id)

        return Response(
            {
                "status": "order created",
                "order_id": order.id,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAdminOrSupplier],
    )
    def change_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status not in Order.Status.values:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = new_status
        order.save()

        return Response(
            {"status": "updated"},
            status=status.HTTP_200_OK,
        )
