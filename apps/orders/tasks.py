from celery import shared_task
from django.core.cache import cache

from . import repositories


@shared_task
def cancel_expired_pending_orders():
    order_ids = repositories.find_expired_pending_order_ids()
    cancelled = 0
    for order_id in order_ids:
        if repositories.cancel_order(order_id):
            cache.delete(f"order:{order_id}")
            cancelled += 1
    return cancelled
