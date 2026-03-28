from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Note
from .serializers import NoteSerializer

class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return notes for the authenticated user."""
        return Note.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Auto assign the authenticated user when creating a new note."""
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="List all user notes",
        description="Retrieve all notes for the authenticated user",
        responses=NoteSerializer(many=True)
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new note",
        description="Create a new note for the authenticated user",
        request=NoteSerializer,
        responses=NoteSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a specific note",
        description="Get details of a specific note by ID",
        responses=NoteSerializer
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a note",
        description="Update an existing note (full update)",
        request=NoteSerializer,
        responses=NoteSerializer
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a note",
        description="Partially update a note (partial update)",
        request=NoteSerializer,
        responses=NoteSerializer
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a note",
        description="Delete a note permanently",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)