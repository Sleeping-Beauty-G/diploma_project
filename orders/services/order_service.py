from django.db import transaction
from products.models import ProductInfo
from orders.models import Order, OrderItem


class OrderService:

    @staticmethod
    def create_order(user, cart, address):
        with transaction.atomic():

            order = Order.objects.create(
                user=user, address=address, status=Order.Status.CONFIRMED
            )

            for item in cart.items.select_related("product"):

                product_info = (
                    ProductInfo.objects.select_for_update()
                    .filter(product=item.product, quantity__gte=item.quantity)
                    .first()
                )

                if not product_info:
                    raise ValueError(f"Not enough stock for {item.product.name}")

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

            return order
