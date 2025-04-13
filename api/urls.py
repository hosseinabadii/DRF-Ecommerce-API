from django.urls import path
from rest_framework.routers import DefaultRouter  # noqa: F401

from api import views_order, views_product, views_user

urlpatterns = [
    path("users/", views_user.UserListView.as_view(), name="user-list"),
    path(
        "products/",
        views_product.ProductListCreateAPIView.as_view(),
        name="product-list",
    ),
    path(
        "products/info/",
        views_product.ProductInfoView.as_view(),
        name="product-info",
    ),
    path(
        "products/<int:product_id>/",
        views_product.ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    # path(
    #     "orders/",
    #     views_order.OrderListCreateAPIView.as_view(),
    #     name="order-list",
    # ),
    # path(
    #     "orders/<uuid:pk>/",
    #     views_order.OrderDetailAPIView.as_view(),
    #     name="order-detail",
    # ),
]


router = DefaultRouter()
router.register(prefix="orders", viewset=views_order.OrderViewSet)
urlpatterns += router.urls


# Related to function based views
# urlpatterns = [
#     path("products/", views_product.product_list, name="product-list"),
#     path("products/info/", views_product.product_info, name="product-info"),
#     path("products/<int:pk>/", views_product.product_detail, name="product-detail"),
#     path("orders/", views_order.order_list, name="order-list"),
#     path("orders/<uuid:pk>/", views_order.order_detail, name="order-detail"),
# ]
