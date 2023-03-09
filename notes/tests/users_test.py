import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
def test_user_create(client):
    response = client.post(
        path='/api/v1/users/',
        data={
            'username': 'test-user',
            'password': 'test-password',
            'last_name': 'last_name',
            'first_name': 'first_name',
            'email': 'user@exmaple.com',
        },
        format='json'
    )

    assert response.status_code == status.HTTP_201_CREATED

    json = response.json()

    assert json.get('username') == 'test-user'
    assert json.get('last_name') == 'last_name'
    assert json.get('last_name') == 'last_name'
    assert json.get('email') == 'user@exmaple.com'
