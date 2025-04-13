import random
from decimal import Decimal

from django.core.management import BaseCommand
from django.utils import lorem_ipsum

from core.models import Order, OrderItem, Product, User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Populating database...")
        Product.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()

        products = [
            Product(
                name="A Scanner Darkly",
                description=lorem_ipsum.paragraph(),
                price=Decimal("12.99"),
                stock=4,
            ),
            Product(
                name="Coffee Machine",
                description=lorem_ipsum.paragraph(),
                price=Decimal("70.99"),
                stock=6,
            ),
            Product(
                name="Velvet Underground & Nico",
                description=lorem_ipsum.paragraph(),
                price=Decimal("15.99"),
                stock=11,
            ),
            Product(
                name="Enter the Wu-Tang (36 Chambers)",
                description=lorem_ipsum.paragraph(),
                price=Decimal("17.99"),
                stock=2,
            ),
            Product(
                name="Digital Camera",
                description=lorem_ipsum.paragraph(),
                price=Decimal("350.99"),
                stock=4,
            ),
            Product(
                name="Watch",
                description=lorem_ipsum.paragraph(),
                price=Decimal("500.05"),
                stock=0,
            ),
        ]

        Product.objects.bulk_create(products)
        products = Product.objects.all()

        user = User.objects.filter(username="admin").first()
        if not user:
            user = User.objects.create_superuser(
                username="admin", password="test", email=None
            )

        for _ in range(3):
            order = Order.objects.create(user=user)
            for product in random.sample(list(products), k=2):
                OrderItem.objects.create(
                    order=order, product=product, quantity=random.randint(1, 3)
                )

        user1 = User.objects.filter(username="test").first()
        if not user1:
            user1 = User.objects.create_user(
                username="test", password="test", email=None, is_staff=True
            )

        for _ in range(3):
            order = Order.objects.create(user=user1)
            for product in random.sample(list(products), k=2):
                OrderItem.objects.create(
                    order=order, product=product, quantity=random.randint(1, 3)
                )

        print("Successfully Done!")
