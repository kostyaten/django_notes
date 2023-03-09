from typing import TypedDict

from rest_framework import serializers

from ...models import Note


class ValidatedData(TypedDict):
    password: str


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'created_at')
