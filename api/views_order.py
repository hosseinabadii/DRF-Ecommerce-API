from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import OrderFilterSet
from api.serializers import OrderCreateSerializer, OrderSerializer
from core.models import Order, User


@extend_schema(tags=["Order"])
class OrderListCreateAPIView(ListCreateAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs if user.is_staff else qs.filter(user=user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer: OrderSerializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Order"])
class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs if user.is_staff else qs.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return OrderCreateSerializer
        return super().get_serializer_class()


@extend_schema(tags=["Order"])
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs if user.is_staff else qs.filter(user=user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OrderCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer: OrderSerializer):
        serializer.save(user=self.request.user)

    @action(methods=["get"], detail=False, url_path="user-orders")
    def user_orders(self, request: Request):
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_list(request: Request):
    user: User = request.user
    orders = Order.objects.prefetch_related("items__product")
    queryset = orders if user.is_staff else orders.filter(user=user)
    order_filterset = OrderFilterSet(data=request.GET, queryset=queryset)
    serializar = OrderSerializer(
        instance=order_filterset.qs,
        many=True,
        context={"request": request},
    )
    return Response(serializar.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request: Request, pk: int):
    user: User = request.user
    if user.is_staff:
        order = get_object_or_404(Order, pk=pk)
    else:
        order = get_object_or_404(Order, pk=pk, user=user)

    serializar = OrderSerializer(instance=order, context={"request": request})
    return Response(serializar.data)
