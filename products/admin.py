from django.contrib import admin

from .models import (
    Category,
    Parameter,
    Product,
    ProductInfo,
    ProductParameter,
)


class ProductParameterInline(admin.TabularInline):
    model = ProductParameter
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
    )

    search_fields = ("name",)
    list_filter = ("category",)


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "supplier",
        "price",
        "quantity",
    )

    list_filter = ("supplier",)
    search_fields = (
        "product__name",
        "supplier__name",
    )

    inlines = [ProductParameterInline]


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = (
        "product_info",
        "parameter",
        "value",
    )

    search_fields = (
        "parameter__name",
        "value",
    )
