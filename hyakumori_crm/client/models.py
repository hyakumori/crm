from typing import Optional, List
import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from pydantic import BaseModel, validator

from ..core.models import (
    TimestampMixin,
    InternalMixin,
    HyakumoriDanticModel,
    HyakumoriDanticUpdateModel,
)


class Client(TimestampMixin, InternalMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = JSONField(default=dict)
    attributes = JSONField(default=dict)
    contacts = models.ManyToManyField(through="ClientContact", to="Contact")

    def add_attribute(self, key, value):
        pass


class Contact(TimestampMixin, InternalMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = JSONField(default=dict)


class RELATIONSHIP_TYPE(models.TextChoices):
    SON = "SON", _("Son")
    DAUGHTER = "DAUGHTER", _("Daughter")
    WIFE = "WIFE", _("Wife")
    HUSBAND = "HUSBAND", _("Husband")
    GRANDSON = "GRANDSON", _("Grandson")
    GRANDDAUGHTER = "GRANDDAUGHTER", _("Granddaughter")
    SISTER = "SISTER", _("Sister")
    BROTHER = "BROTHER", _("Brother")


class ClientContact(TimestampMixin, models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE)
    attributes = JSONField(default=dict)
    relationship_type = models.CharField(
        max_length=20, choices=RELATIONSHIP_TYPE.choices, null=True
    )


class ClientProfileCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]
    home_number: Optional[str]
    mobile_number: Optional[str]


class ContactCreate(BaseModel):
    internal_id: Optional[str]
    profile: ClientProfileCreate
    relationship_type: RELATIONSHIP_TYPE


class ClientCreate(HyakumoriDanticModel):
    internal_id: Optional[str]
    profile: ClientProfileCreate
    attributes: Optional[dict]
    contacts: Optional[List[ContactCreate]]


class ClientUpdate(HyakumoriDanticUpdateModel, ClientCreate):
    pass


class ClientRead(HyakumoriDanticModel):
    id: str
    internal_id: Optional[str]
    profile: ClientProfileCreate
    attributes: dict = {}
