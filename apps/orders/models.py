from django.db import models


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "pending"),
        ("confirmed", "confirmed"),
        ("cancelled", "cancelled"),
    )

    user_id = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    idempotency_key = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.BigIntegerField()
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "order_items"
