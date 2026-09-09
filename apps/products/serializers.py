from rest_framework import serializers


class ProductCreateSerializer(serializers.Serializer):
    """POST /products request validatsiyasi.

    TODO:
    - name: CharField, max_length=255, required
    - price: DecimalField(max_digits=12, decimal_places=2), min_value=0
    - stock_quantity: IntegerField, min_value=0
    """


class ProductResponseSerializer(serializers.Serializer):
    """Response shape: id, name, price, stock_quantity, created_at."""
