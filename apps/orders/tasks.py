"""Celery tasks — fon jarayonlar."""

from celery import shared_task


@shared_task
def cancel_expired_pending_orders():
    """15 daqiqadan ortiq pending qolgan orderlarni cancel qilish.

    TODO:
    1. repositories.find_expired_pending_order_ids() chaqirish
    2. Har biri uchun services.cancel_order(order_id) chaqirish
       (yoki to'g'ridan-to'g'ri repositories.cancel_order, xohishga qarab)
    3. Har bir order uchun natijani logga yozish

    config/celery.py dagi beat_schedule ichida bu task har 1 daqiqada
    ishga tushishi kerak (crontab(minute="*/1")).
    """
    raise NotImplementedError
