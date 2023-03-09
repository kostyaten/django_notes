from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from ..serializers import NoteSerializer
from ...models import Note


@extend_schema(tags=['notes'])
class NoteViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    """Заметки"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
