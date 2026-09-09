"""Handler/controller qatlami — faqat request parse, service chaqirish,
response qaytarish. Business logika bu yerda bo'lmasligi kerak."""

from rest_framework.views import APIView


class ProductListCreateView(APIView):
    """POST /products

    TODO:
    1. ProductCreateSerializer bilan validatsiya
    2. services.create_product(...) chaqirish
    3. 201 + ProductResponseSerializer natija qaytarish
    """

    def post(self, request):
        raise NotImplementedError
