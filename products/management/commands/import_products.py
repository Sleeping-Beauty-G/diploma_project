import os
import yaml

from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User
from suppliers.models import Supplier

from products.models import (
    Category,
    Product,
    ProductInfo,
    Parameter,
    ProductParameter,
)


class Command(BaseCommand):
    help = "Import products from YAML"

    def handle(self, *args, **kwargs):

        file_path = os.path.join(settings.BASE_DIR, "shop_data.yaml")

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR("File not found"))
            return

        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        for item in data.get("products", []):

            category = None

            if item.get("category"):
                category, _ = Category.objects.get_or_create(name=item["category"])

            product, _ = Product.objects.get_or_create(
                name=item["name"],
                defaults={
                    "description": item.get("description", ""),
                    "category": category,
                },
            )

            supplier_username = item["supplier"].lower().replace(" ", "_")

            supplier_user, _ = User.objects.get_or_create(
                username=supplier_username,
                defaults={
                    "email": f"{supplier_username}@example.com",
                    "role": "supplier",
                },
            )

            supplier, _ = Supplier.objects.get_or_create(
                name=item["supplier"],
                defaults={
                    "user": supplier_user,
                },
            )

            product_info, _ = ProductInfo.objects.update_or_create(
                product=product,
                supplier=supplier,
                defaults={
                    "price": item["price"],
                    "quantity": item.get("stock", 0),
                },
            )

            for key, value in item.get("parameters", {}).items():

                parameter, _ = Parameter.objects.get_or_create(name=key)

                ProductParameter.objects.update_or_create(
                    product_info=product_info,
                    parameter=parameter,
                    defaults={
                        "value": str(value),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Import completed"))
