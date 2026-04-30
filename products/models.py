from django.db import models
from suppliers.models import Supplier


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    """
    Предложение товара от поставщика
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_infos"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="product_infos"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("product", "supplier")

    def __str__(self):
        return f"{self.product} - {self.supplier}"



class Parameter(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class ProductParameter(models.Model):
    product_info = models.ForeignKey(
        ProductInfo,
        related_name="parameters",
        on_delete=models.CASCADE
    )
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.parameter}: {self.value}"

