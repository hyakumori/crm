from django.db import models
from django.contrib.postgres.fields import JSONField
from hyakumori_crm.core.models import AttributesMixin, TimestampMixin


class Oauth(TimestampMixin, AttributesMixin, models.Model):
    access_token = models.CharField(max_length=255)
    team_id = models.CharField(max_length=11, db_index=True)
    team_name = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    incoming_webhook = JSONField()
    bot_user_id = models.CharField(max_length=11)
    authed_user_id = models.CharField(max_length=11)
