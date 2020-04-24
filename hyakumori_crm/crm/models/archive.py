from django.db import models

from ...core.models import BaseResourceModel


class Archive(BaseResourceModel):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    archive_date = models.DateField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    future_response = models.CharField(max_length=255, blank=True)

    class Meta:
        permissions = [
            ("manage_archive", "All permissions for archive"),
        ]
