from drf_spectacular.utils import extend_schema
from rest_framework import generics

from api.serializers import UserSerializer
from core.models import User


@extend_schema(tags=["User"])
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
