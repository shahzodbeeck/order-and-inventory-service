from rest_framework.views import APIView


class OrderCreateView(APIView):
    def post(self, request):
        raise NotImplementedError


class OrderDetailView(APIView):
    def get(self, request, order_id):
        raise NotImplementedError


class OrderCancelView(APIView):
    def post(self, request, order_id):
        raise NotImplementedError
