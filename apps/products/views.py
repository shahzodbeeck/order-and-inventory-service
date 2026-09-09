"""Handler/controller qatlami — faqat request parse, service chaqirish,
response qaytarish. Business logika bu yerda bo'lmasligi kerak."""

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .serializers import ProductCreateSerializer, ProductResponseSerializer


class ProductListCreateView(APIView):
    """POST /products"""

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = services.create_product(**serializer.validated_data)

        response = ProductResponseSerializer(product)
        return Response(response.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    """GET /products/{id}"""

    def get(self, request, product_id: int):
        try:
            product = services.get_product(product_id)
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        response = ProductResponseSerializer(product)
        return Response(response.data, status=status.HTTP_200_OK)
