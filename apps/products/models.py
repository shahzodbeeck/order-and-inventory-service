# Bu model ORM query uchun emas, faqat Django admin/introspection va
# migration state uchun. Barcha CRUD/business query'lar repositories.py
# ichida raw SQL bilan yoziladi (managed=False -> migration jadval yaratmaydi,
# jadval db/schema.sql orqali yaratiladi).

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "products"
