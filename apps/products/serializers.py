from rest_framework import serializers


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    stock_quantity = serializers.IntegerField(min_value=0)


class ProductResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    stock_quantity = serializers.IntegerField()
    created_at = serializers.DateTimeField()
