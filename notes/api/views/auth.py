from typing import Any

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..serializers import AuthSerializer, AuthResponseSerializer, AuthDestroySerializer

User = get_user_model()


@extend_schema(tags=['auth'])
class AuthViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    """Аутентификация пользователя"""

    serializer_class = AuthSerializer
    lookup_field = 'username'
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'destroy':
            return AuthDestroySerializer
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(), ]

        return super().get_permissions()

    def get_object(self):
        if self.action == 'destroy':
            username = self.kwargs.get('username')
            user = get_object_or_404(User, username=username)
            return get_object_or_404(Token, user=user)

    @extend_schema(
        request=AuthSerializer,
        responses={
            201: AuthResponseSerializer,
        },
        methods=['POST']
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.create(serializer.validated_data)

        response = AuthResponseSerializer({'access_token': token})
        return Response(response.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description='Завершение сессии для пользователя, предполагается что имя пользователя будет известно фронту'
    )
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=kwargs)
        serializer.is_valid(raise_exception=True)

        token = get_object_or_404(Token, key=request.auth.key)

        if serializer.validated_data.get('username') != token.user.username:
            raise AuthenticationFailed(detail='It is not possible to delete a user session')

        self.perform_destroy(instance=instance)
        return Response({})
