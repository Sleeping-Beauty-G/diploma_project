from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartItemSerializer, OrderSerializer
from products.models import ProductInfo
from .tasks import send_order_email_task


# 🔐 Permissions
class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "client"


# 🛒 Cart
class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


# 📦 Orders
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")

    # 🧾 Checkout
    @action(detail=False, methods=["post"])
    def checkout(self, request):
        user = request.user

        try:
            cart = Cart.objects.prefetch_related("items__product").get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)

        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        address = request.data.get("address")
        if not address:
            return Response({"error": "Address required"}, status=400)

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                address=address,
                status=Order.Status.CONFIRMED
            )

            for item in cart.items.all():
                product_info = ProductInfo.objects.select_for_update().filter(
                    product=item.product,
                    quantity__gte=item.quantity
                ).select_related("supplier").first()

                if not product_info:
                    return Response(
                        {"error": f"Not enough stock for {item.product.name}"},
                        status=400
                    )

                product_info.quantity -= item.quantity
                product_info.save()

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    supplier=product_info.supplier,
                    quantity=item.quantity,
                    price=product_info.price
                )

            cart.items.all().delete()

        send_order_email_task.delay(user.email, order.id)

        return Response(
            {"status": "order created", "order_id": order.id},
            status=201
        )

    # 🔄 Change status
    @action(detail=True, methods=["patch"])
    def change_status(self, request, pk=None):
        order = self.get_object()

        new_status = request.data.get("status")

        if new_status not in Order.Status.values:
            return Response({"error": "Invalid status"}, status=400)

        order.status = new_status
        order.save()

        return Response({"status": "updated"})