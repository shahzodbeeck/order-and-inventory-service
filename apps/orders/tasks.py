from celery import shared_task


@shared_task
def cancel_expired_pending_orders():
    raise NotImplementedError
