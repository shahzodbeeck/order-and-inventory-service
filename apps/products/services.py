"""Products business logic. View'lar to'g'ridan-to'g'ri repository'ni
emas, shu qatlamni chaqiradi."""

from . import repositories


def create_product(name: str, price, stock_quantity: int) -> dict:
    """TODO: validatsiyadan o'tgan datani repositories.create_product'ga uzatish."""
    raise NotImplementedError


def get_product(product_id: int) -> dict:
    """TODO: repositories.get_product_by_id chaqirish, topilmasa 404 uchun
    xato ko'tarish (masalan ObjectDoesNotExist yoki custom exception)."""
    raise NotImplementedError
