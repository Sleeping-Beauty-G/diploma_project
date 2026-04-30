import yaml
import os
from django.conf import settings
from django.core.management.base import BaseCommand

from suppliers.models import Supplier
from products.models import Product, ProductInfo


class Command(BaseCommand):
    help = "Import products from YAML file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "shop_data.yaml")

        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        for item in data["products"]:
            supplier, _ = Supplier.objects.get_or_create(
                name=item["supplier"]
            )

            product, _ = Product.objects.get_or_create(
                name=item["name"]
            )

            ProductInfo.objects.create(
                product=product,
                supplier=supplier,
                price=item["price"],
                quantity=item["stock"]
            )

        self.stdout.write(self.style.SUCCESS("Import completed"))