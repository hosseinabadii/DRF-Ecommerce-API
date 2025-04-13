from django.db.models import Max
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import ProductFilterSet
from api.serializers import ProductInfoSerializer, ProductSerializer
from core.models import Product


@extend_schema(tags=["Product"])
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.order_by("pk")
    serializer_class = ProductSerializer
    filterset_class = ProductFilterSet
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price"]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    pagination_class.page_size = 4
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 20


@extend_schema(tags=["Product"])
class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


@extend_schema(tags=["Product"])
class ProductInfoView(APIView):
    def get(self, request: Request):
        products = Product.objects.all()
        instance = {
            "products": products,
            "count": len(products),
            "max_price": products.aggregate(max_price=Max("price"))["max_price"],
        }
        serializar = ProductInfoSerializer(instance=instance)
        return Response(serializar.data)


@api_view(["GET"])
def product_list(request: Request):
    product_filterset = ProductFilterSet(
        data=request.GET,
        queryset=Product.objects.all(),
    )
    serializar = ProductSerializer(instance=product_filterset.qs, many=True)
    return Response(serializar.data)


@api_view(["GET"])
def product_detail(request: Request, pk: int):
    product = get_object_or_404(Product, pk=pk)
    serializar = ProductSerializer(instance=product)
    return Response(serializar.data)


@api_view(["GET"])
def product_info(request: Request):
    products = Product.objects.all()
    data = {
        "products": products,
        "count": len(products),
        "max_price": products.aggregate(max_price=Max("price"))["max_price"],
    }
    serializar = ProductInfoSerializer(instance=data)
    return Response(serializar.data)
