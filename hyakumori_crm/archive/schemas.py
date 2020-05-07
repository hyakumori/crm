from datetime import datetime
from typing import Optional, List
from uuid import UUID

from django.utils.translation import gettext_lazy as _
from pydantic import validator, root_validator

from ..core.models import HyakumoriDanticModel
from ..crm.models import (
    Archive,
    Contact,
    CustomerContact,
    ArchiveCustomer,
    ArchiveCustomerContact,
)


class ArchiveInput(HyakumoriDanticModel):
    title: str
    content: Optional[str]
    location: Optional[str]
    future_action: Optional[str]
    archive_date: Optional[datetime]


class ArchiveFilter(HyakumoriDanticModel):
    id: str = None
    sys_id: str = None
    archive_date: str = None
    title: str = None
    content: str = None
    author: str = None
    location: str = None
    their_participants: str = None
    our_participants: str = None
    associated_forest: str = None

    class Config:
        arbitrary_types_allowed = True
        min_anystr_length = 0


class ArchiveContact(HyakumoriDanticModel):
    contact_id: UUID
    customer_id: Optional[UUID]


class ArchiveCustomerInput(HyakumoriDanticModel):
    archive: Archive
    added: List[ArchiveContact] = []
    deleted: List[ArchiveContact] = []

    class Config:
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def inject_archive(cls, values):
        if not values.get("archive"):
            return values
        cls.archive = values["archive"]
        return values

    @validator("deleted", each_item=True)
    def check_deleted(cls, v):
        try:
            contact = Contact.objects.get(id=v.contact_id)
        except Contact.DoesNotExist:
            raise ValueError(_("Contact {} not found").format(v.contact_id))
        if v.customer_id:
            try:
                cc = contact.customercontact_set.get(customer_id=v.customer_id)
            except CustomerContact.DoesNotExist:
                raise ValueError(_("Customer {} not found").format(v.customer_id))
        else:
            try:
                cc = contact.customercontact_set.get(is_basic=True)
                v.customer_id = cc.customer_id
            except CustomerContact.DoesNotExist:
                raise ValueError(_("Contact {} not found").format(v.contact_id))
        try:
            ac = cls.archive.archivecustomer_set.get(customer_id=v.customer_id)
        except ArchiveCustomer.DoesNotExist:
            raise ValueError(_("Contact {} not found").format(v.contact_id))
        try:
            ac.archivecustomercontact_set.get(customercontact_id=cc.id)
        except ArchiveCustomerContact.DoesNotExist:
            raise ValueError(_("Contact {} not found").format(v.contact_id))
        return v

    @validator("added", each_item=True)
    def check_added(cls, v):
        try:
            contact = Contact.objects.get(id=v.contact_id)
        except Contact.DoesNotExist:
            raise ValueError(_("Contact {} not found").format(v.contact_id))
        if v.customer_id:
            try:
                contact.customercontact_set.get(customer_id=v.customer_id)
            except CustomerContact.DoesNotExist:
                raise ValueError(_("Customer {} not found").format(v.customer_id))
        else:
            try:
                cc = contact.customercontact_set.get(is_basic=True)
                v.customer_id = cc.customer_id
            except CustomerContact.DoesNotExist:
                raise ValueError(_("Contact {} not found").format(v.contact_id))
        return v
