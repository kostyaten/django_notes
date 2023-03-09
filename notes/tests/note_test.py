import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from notes.models import Note

User = get_user_model()


@pytest.mark.django_db
def test_note_create(client_auth):

    response = client_auth.post(
        path='/api/v1/note/',
        data={
            'title': 'title',
            'description': 'description',
        },
        format='json'
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Note.objects.filter(user__username='test-user').exists()


@pytest.mark.django_db
def test_note(client_auth):
    response = client_auth.post(
        path='/api/v1/note/',
        data={
            'title': 'title',
            'description': 'description',
        },
        format='json'
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = client_auth.get(
        path='/api/v1/note/',
        format='json'
    )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    assert json.get('count') == 1
    assert json.get('results')[0].get('id') == 1
    assert json.get('results')[0].get('title') == 'title'
    assert json.get('results')[0].get('description') == 'description'
    assert json.get('results')[0].get('created_at')

    # Получаем отдельную запись
    response = client_auth.get(
        path='/api/v1/note/1/',
        format='json'
    )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    assert json.get('id') == 1
    assert json.get('title') == 'title'
    assert json.get('description') == 'description'
    assert json.get('created_at')

    # Удаляем
    response = client_auth.delete(
        path='/api/v1/note/1/',
        format='json'
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client_auth.get(
        path='/api/v1/note/1/',
        format='json'
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
