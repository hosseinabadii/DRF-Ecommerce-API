import uuid
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveSmallIntegerField()

    @property
    def in_stock(self) -> bool:
        return self.stock > 0

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    class StatusChoises(models.TextChoices):
        PENDING = "pending"
        CONFIRMED = "confirmed"
        CANCELLED = "cancelled"

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=StatusChoises.choices, default=StatusChoises.PENDING
    )

    products = models.ManyToManyField(
        Product,
        through="OrderItem",
        related_name="orders",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Order{self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    @property
    def item_subtotal(self) -> Decimal:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"
