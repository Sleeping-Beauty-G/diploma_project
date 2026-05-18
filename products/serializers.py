from rest_framework import serializers

from .models import (
    Product,
    ProductInfo,
    ProductParameter,
)


class ProductParameterSerializer(serializers.ModelSerializer):

    parameter = serializers.CharField(source="parameter.name")

    class Meta:
        model = ProductParameter
        fields = ["parameter", "value"]


class ProductInfoSerializer(serializers.ModelSerializer):

    parameters = ProductParameterSerializer(
        source="productparameter_set",
        many=True,
        read_only=True,
    )

    class Meta:
        model = ProductInfo
        fields = [
            "id",
            "product",
            "supplier",
            "price",
            "quantity",
            "parameters",
        ]


class ProductSerializer(serializers.ModelSerializer):

    product_infos = ProductInfoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "product_infos",
        ]
        depth = 1
