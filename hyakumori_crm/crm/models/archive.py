from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from ...core.models import BaseResourceModel


class Archive(BaseResourceModel):

    consult_date = models.DateField(blank=True)
    location = JSONField( blank=True, null=True)
    future_action = models.CharField(max_length=5000, blank=True)
    discuss_content = models.CharField(max_length=5000, blank=True)
    attachment_list = GenericRelation('Attachment', related_name='archive')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_archives",
        verbose_name="creator",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    class Meta:
        permissions = [
            ("manage_archive", "All permissions for archive"),
        ]
