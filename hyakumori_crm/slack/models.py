from django.db import models
from django.contrib.postgres.fields import JSONField


class Oauth(models.Model):
    access_token = models.CharField(max_length=255)
    team_id = models.CharField(max_length=11)
    team_name = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    incoming_webhook = JSONField()
    bot_user_id = models.CharField()
