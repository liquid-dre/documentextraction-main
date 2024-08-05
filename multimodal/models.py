import base64
from django.db import models

from django.core.exceptions import ValidationError

def validate_base64_string(value):
    try:
        base64.b64decode(value)
    except (TypeError, ValueError):
        raise ValidationError('Invalid base64 string')

class DocumentToRead(models.Model):
    url = models.CharField(max_length=255, null=True, blank=True)
    base64_string = models.TextField(validators=[validate_base64_string], default='')
    prompt_description = models.TextField()

    def __str__(self):
        return self.url + ' ' + self.prompt_description