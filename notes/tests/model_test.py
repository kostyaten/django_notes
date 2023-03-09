import pytest
from django.contrib.auth import get_user_model

from ..models import Note

User = get_user_model()


@pytest.mark.django_db
def test_model_note():
    user = User.objects.create(username='test-user')

    note = Note.objects.create(user=user, title='Title', description='Description')
    assert note.created_at
    assert note.title == 'Title'
    assert note.description == 'Description'
    assert note.user.username == 'test-user'
    assert str(note) == 'Title'
