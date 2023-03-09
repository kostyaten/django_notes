import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
def client_auth() -> APIClient:
    user = User.objects.create(username='test-user')
    user.set_password('test-password')
    user.save()

    token, _ = Token.objects.get_or_create(user=user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.key}')
    return client
