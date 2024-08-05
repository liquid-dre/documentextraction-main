# purpose of this isability to serialize objects/models 
from rest_framework import serializers
from .models import DocumentToRead

class DocumentToReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentToRead
        fields = ['id', 'url','base64_string', 'prompt_description']