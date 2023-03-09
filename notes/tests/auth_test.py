import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()


@pytest.mark.django_db
def test_auth_create(client):
    user = User.objects.create(username='test-user')
    user.set_password('test-password')
    user.save()

    response = client.post(
        path='/api/v1/auth/',
        data={
            'username': 'test-user',
            'password': 'test-password',
        },
        format='json'
    )
    assert response.json().get('access_token')
    assert len(response.json().get('access_token')) == 40


@pytest.mark.django_db
def test_auth_create_incorrect_username_or_password(client):
    user = User.objects.create(username='test-user')
    user.set_password('test-password')
    user.save()

    response = client.post(
        path='/api/v1/auth/',
        data={
            'username': 'test-user',
            'password': 'test-password-fail',
        },
        format='json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_auth_logout(client):
    user = User.objects.create(username='test-user')
    user.set_password('test-password')
    user.save()
    token, _ = Token.objects.get_or_create(user=user)

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.key}')

    response = client.delete(
        path=f'/api/v1/auth/{user.username}/',
        format='json'
    )
    assert response.status_code == status.HTTP_200_OK

    assert not Token.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_auth_logout_fail(client):
    user = User.objects.create(username='test-user')
    user.set_password('test-password')
    user.save()

    user2 = User.objects.create(username='test-user2')
    user2.set_password('test-password')
    user2.save()

    Token.objects.get_or_create(user=user)
    token, _ = Token.objects.get_or_create(user=user2)

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.key}')

    response = client.delete(path=f'/api/v1/auth/{user.username}/', format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
