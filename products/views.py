from rest_framework import viewsets
from .models import Product, ProductInfo
from .serializers import ProductSerializer, ProductInfoSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.prefetch_related(
        'product_infos__parameters__parameter'
    )
    serializer_class = ProductSerializer


class ProductInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductInfo.objects.select_related('supplier', 'product')
    serializer_class = ProductInfoSerializer
