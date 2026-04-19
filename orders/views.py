from rest_framework import viewsets, permissions, status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .models import Cart, CartItem, Order, OrderItem
from products.models import ProductInfo
from .serializers import CartSerializer, OrderSerializer
from .tasks import send_order_email_task


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def list(self, request):
        cart = self.get_cart(request.user)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["post"])
    def add(self, request):
        cart = self.get_cart(request.user)

        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "product_id required"}, status=400)

        if quantity <= 0:
            return Response({"error": "quantity must be > 0"}, status=400)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={"quantity": quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response({"status": "added"})


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

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
                product_info = ProductInfo.objects.filter(
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