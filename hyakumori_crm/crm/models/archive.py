from django.db import models

from ...core.models import BaseResourceModel


class Archive(BaseResourceModel):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(null=True)
    archive_date = models.DateTimeField(null=True)
    location = models.CharField(max_length=255, null=True)
    future_response = models.CharField(max_length=255, null=True)

    class Meta:
        permissions = [
            ("manage_archive", "All permissions for archive"),
        ]
