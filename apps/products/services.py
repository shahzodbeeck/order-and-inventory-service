"""Products business logic. View'lar to'g'ridan-to'g'ri repository'ni
emas, shu qatlamni chaqiradi."""

from django.core.exceptions import ObjectDoesNotExist

from . import repositories


def create_product(name: str, price, stock_quantity: int) -> dict:
    return repositories.create_product(name, price, stock_quantity)


def get_product(product_id: int) -> dict:
    product = repositories.get_product_by_id(product_id)
    if product is None:
        raise ObjectDoesNotExist(f"Product {product_id} not found")
    return product
