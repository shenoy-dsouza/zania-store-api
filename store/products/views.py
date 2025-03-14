from rest_framework import generics
from store.products.serializers import ProductsSerializer
from store.products.models import Product
from django_filters import rest_framework as django_filters
from store.products.filters import ProductFilter
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from store import error_codes
from store.exceptions import BaseException
from rest_framework.serializers import ValidationError


class ProductsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductsSerializer
    queryset = Product.objects.all()
    filter_backends = [
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
    ]

    filterset_class = ProductFilter
    ordering_fields = [
        "name",
        "stock",
        "price",
        "created",
    ]

    ordering = ["-created"]

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except BaseException as e:
            return Response(
                {
                    "status": "error",
                    "code": e.get_error_code(),
                    "message": str(e),
                    "errors": e.get_errors(),
                },
                e.get_http_status_code(),
            )

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {
                    "status": "success",
                    "message": "Product created.",
                    "data": serializer.data,
                },
                status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response(
                {
                    "errors": e.detail,
                    "code": error_codes.VALIDATION_ERROR,
                },
                status.HTTP_400_BAD_REQUEST,
            )

        except BaseException as e:
            return Response(
                {
                    "status": "error",
                    "code": e.get_error_code(),
                    "message": str(e),
                    "errors": e.get_errors(),
                },
                e.get_http_status_code(),
            )
