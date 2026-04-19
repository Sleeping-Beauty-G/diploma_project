from rest_framework import serializers
from .models import Product, ProductInfo, ProductParameter, Parameter


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = ParameterSerializer()

    class Meta:
        model = ProductParameter
        fields = ['parameter', 'value']


class ProductInfoSerializer(serializers.ModelSerializer):
    parameters = ProductParameterSerializer(many=True, read_only=True)
    supplier = serializers.StringRelatedField()

    class Meta:
        model = ProductInfo
        fields = ['id', 'supplier', 'price', 'quantity', 'parameters']


class ProductSerializer(serializers.ModelSerializer):
    product_infos = ProductInfoSerializer(many=True, read_only=True)  # ✅ теперь совпадает

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'product_infos']