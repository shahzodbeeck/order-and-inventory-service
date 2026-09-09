from rest_framework import serializers


class OrderItemInputSerializer(serializers.Serializer):
    """TODO: product_id (IntegerField), quantity (IntegerField, min_value=1)."""


class OrderCreateSerializer(serializers.Serializer):
    """POST /orders body validatsiyasi.

    TODO:
    - items: OrderItemInputSerializer(many=True), min 1 ta item
    - Idempotency-Key headerdan olinadi (bodyda emas, view'da o'qiladi)
    """


class OrderResponseSerializer(serializers.Serializer):
    """Response: id, status, items[], created_at, expires_at."""
