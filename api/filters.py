import django_filters
from django.db.models import Q, QuerySet
from rest_framework.filters import BaseFilterBackend

from core.models import Order, Product


class ProductFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        method="filter_name",
        label="Name",
    )
    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
        label="Minimum Price",
    )
    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
        label="Maximum Price",
    )

    def filter_name(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        return queryset.filter(Q(name__iexact=value) | Q(name__icontains=value))

    class Meta:
        model = Product
        fields = ["name", "min_price", "max_price"]


class OrderFilterSet(django_filters.FilterSet):
    created_at = django_filters.DateFilter(
        field_name="created_at__date",
        lookup_expr="exact",
        label="Created At",
    )
    created_before = django_filters.DateFilter(
        field_name="created_at__date",
        lookup_expr="lte",
        label="Created Before",
    )
    created_after = django_filters.DateFilter(
        field_name="created_at__date",
        lookup_expr="gte",
        label="Created After",
    )

    class Meta:
        model = Order
        fields = ["status", "created_at", "created_before", "created_after"]


class InStockFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
