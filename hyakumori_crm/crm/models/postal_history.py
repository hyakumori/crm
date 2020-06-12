from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from ...core.models import BaseResourceModel, BaseRelationModel


class PostalHistory(BaseResourceModel):
    title = models.CharField(max_length=255, blank=True)
    future_action = models.CharField(max_length=255, null=True)
    archive_date = models.DateTimeField(null=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, default=None, null=True
    )
    tags = JSONField(default=dict, encoder=DjangoJSONEncoder)

    class Meta:
        permissions = [
            ("manage_postal_history", "All permissions for postal history"),
        ]


class PostalHistoryForest(BaseRelationModel):
    archive = models.ForeignKey("PostalHistory", on_delete=models.PROTECT)
    forest = models.ForeignKey("Forest", on_delete=models.CASCADE)


class PostalHistoryCustomer(BaseRelationModel):
    archive = models.ForeignKey("PostalHistory", on_delete=models.PROTECT)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)


class PostalHistoryCustomerContact(BaseRelationModel):
    archivecustomer = models.ForeignKey(
        "PostalHistoryCustomer", on_delete=models.CASCADE
    )
    customercontact = models.ForeignKey("CustomerContact", on_delete=models.CASCADE)


class PostalHistoryUser(BaseRelationModel):
    archive = models.ForeignKey("PostalHistory", on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
