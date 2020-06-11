from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from ...core.models import BaseResourceModel


class PostalHistory(BaseResourceModel):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(null=True)
    archive_date = models.DateTimeField(null=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, default=None, null=True
    )
    tags = JSONField(default=dict, encoder=DjangoJSONEncoder)

    class Meta:
        permissions = [
            ("manage_postal_history", "All permissions for postal history"),
        ]
