from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from core.models import Order, OrderItem, Product, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "stock", "in_stock")

    def validate_price(self, value: Decimal) -> Decimal:
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ("product", "quantity")

    items = OrderItemCreateSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ("order_id", "status", "items")
        extra_kwargs = {
            "order_id": {"read_only": True},
            "status": {"read_only": True},
        }

    def create(self, validated_data: dict):
        orderitem_data = validated_data.pop("items", None)
        with transaction.atomic():
            created_order = super().create(validated_data)
            if orderitem_data is not None:
                for item in orderitem_data:
                    OrderItem.objects.create(order=created_order, **item)
        return created_order

    def update(self, order: Order, validated_data: dict):
        orderitem_data = validated_data.pop("items", None)
        with transaction.atomic():
            updated_order = super().update(order, validated_data)
            if orderitem_data is not None:
                updated_order.items.all().delete()
                for item in orderitem_data:
                    OrderItem.objects.create(order=updated_order, **item)
        return updated_order


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.price"
    )

    class Meta:
        model = OrderItem
        fields = ("product_name", "product_price", "quantity", "item_subtotal")


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    order_url = serializers.HyperlinkedIdentityField(view_name="order-detail")
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "order_id",
            "order_url",
            "user",
            "created_at",
            "status",
            "items",
            "total_price",
        )

    def get_total_price(self, order: Order) -> Decimal:
        return sum(item.item_subtotal for item in order.items.all())
