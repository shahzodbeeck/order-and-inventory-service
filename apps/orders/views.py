"""Handler/controller qatlami."""

from rest_framework.views import APIView


class OrderCreateView(APIView):
    """POST /orders

    TODO:
    1. Idempotency-Key headerini o'qish, bo'lmasa 400 qaytarish
    2. OrderCreateSerializer bilan validatsiya
    3. services.create_order(user_id=request.user.id, idempotency_key=..., items=...)
    4. Stock yetmasa -> 409 (yoki 422, talabga qarab tanlang, README'da izohlang)
    5. Muvaffaqiyatli -> 201 + order data
    """

    def post(self, request):
        raise NotImplementedError


class OrderDetailView(APIView):
    """GET /orders/{id}

    TODO:
    1. services.get_order(order_id) chaqirish
    2. Topilmasa 404
    """

    def get(self, request, order_id: int):
        raise NotImplementedError


class OrderCancelView(APIView):
    """POST /orders/{id}/cancel

    TODO:
    1. services.cancel_order(order_id) chaqirish
    2. Status pending bo'lmasa -> 409
    """

    def post(self, request, order_id: int):
        raise NotImplementedError
