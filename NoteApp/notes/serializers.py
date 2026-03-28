from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'title': {
                'help_text': 'The title of the note (max 200 characters)',
                'required': True,
            },
            'content': {
                'help_text': 'The content/body of the note',
                'required': True,
            },
            'created_at': {
                'help_text': 'Timestamp when the note was created',
            },
            'updated_at': {
                'help_text': 'Timestamp when the note was last updated',
            },
        }