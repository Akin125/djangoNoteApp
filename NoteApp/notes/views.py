from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Note
from .serializers import NoteSerializer

# Create your views here.
class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return notes for the authenticated user."""
        return Note.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Auto assign the authenticated user when creating a new note."""
        serializer.save(user=self.request.user)

