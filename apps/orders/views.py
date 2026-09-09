from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .serializers import OrderCreateSerializer


class OrderCreateView(APIView):
    def post(self, request):
        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key:
            return Response(
                {"detail": "Idempotency-Key header is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items = [
            {"product_id": item["product_id"], "quantity": item["quantity"]}
            for item in serializer.validated_data["items"]
        ]

        try:
            result = services.create_order(request.user.id, idempotency_key, items)
        except services.InsufficientStockError:
            return Response(
                {"detail": "Insufficient stock for one or more items"},
                status=status.HTTP_409_CONFLICT,
            )
        except services.IdempotencyInProgressError:
            return Response(
                {"detail": "A request with this Idempotency-Key is already being processed"},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(result["body"], status=result["response_code"])


class OrderDetailView(APIView):
    def get(self, request, order_id):
        order = services.get_order(order_id)
        if order is None:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(order, status=status.HTTP_200_OK)


class OrderCancelView(APIView):
    def post(self, request, order_id):
        try:
            order = services.cancel_order(order_id)
        except services.OrderNotCancellableError:
            return Response(
                {"detail": "Order cannot be cancelled (not pending or not found)"},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(order, status=status.HTTP_200_OK)
