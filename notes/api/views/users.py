from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from ..serializers import UserSerializer


@extend_schema(tags=['users'])
class UserViewSet(GenericViewSet, mixins.CreateModelMixin):
    """Создание пользователя"""

    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
