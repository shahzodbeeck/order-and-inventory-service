import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("order_system")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "cancel-expired-pending-orders": {
        "task": "apps.orders.tasks.cancel_expired_pending_orders",
        "schedule": crontab(minute="*/1"),
    },
}
