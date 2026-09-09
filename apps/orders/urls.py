from django.urls import path

from .views import OrderCancelView, OrderCreateView, OrderDetailView

urlpatterns = [
    path("orders", OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:order_id>", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:order_id>/cancel", OrderCancelView.as_view(), name="order-cancel"),
]
