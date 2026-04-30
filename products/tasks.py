from celery import shared_task
import yaml
from .models import Product, ProductInfo, Parameter, ProductParameter
from suppliers.models import Supplier


@shared_task
def import_products(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        for item in data.get('products', []):
            product, _ = Product.objects.get_or_create(
                name=item['name']
            )

            supplier, _ = Supplier.objects.get_or_create(
                name=item['supplier']
            )

            product_info, _ = ProductInfo.objects.update_or_create(
                product=product,
                supplier=supplier,
                defaults={
                    'price': item['price'],
                    'quantity': item.get('stock', 0)
                }
            )

            # характеристики
            for param_name, value in item.get('parameters', {}).items():
                parameter, _ = Parameter.objects.get_or_create(name=param_name)

                ProductParameter.objects.update_or_create(
                    product_info=product_info,
                    parameter=parameter,
                    defaults={'value': value}
                )

    except Exception as e:
        print(f'Import error: {e}')

