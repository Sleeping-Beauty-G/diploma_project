from celery import shared_task
import yaml

from users.models import User
from suppliers.models import Supplier
from .models import (
    Product,
    ProductInfo,
    Parameter,
    ProductParameter,
)


@shared_task
def import_products(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        for item in data.get("products", []):

            product, _ = Product.objects.get_or_create(
                name=item["name"],
                defaults={
                    "description": item.get("description", ""),
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

    except Exception as error:
        print(f"Import error: {error}")
