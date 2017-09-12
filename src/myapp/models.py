"""All models for myapp Django application.
"""
from django.db import models


class Crisis(models.Model):
    """Represents a crisis that happens in real life."""
    crisis_name = models.CharField(max_length=30)
