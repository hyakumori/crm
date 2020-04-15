from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.db.models import OuterRef, Subquery

from ...core.models import BaseResourceModel, BaseQuerySet
from ..schemas.customer import Address, Banking
from ..schemas.customer import Contact as ContactSchema
from ..schemas.customer import Name
from .relations import CustomerContact


class DefaultCustomer:
    @staticmethod
    def name_kanji():
        return Name().dict()

    @staticmethod
    def name_kana():
        return Name().dict()

    @staticmethod
    def address():
        return Address().dict()

    @staticmethod
    def banking():
        return Banking().dict()


class DefaultContact:
    @staticmethod
    def contact_info():
        return ContactSchema().dict()


class CustomerQueryset(BaseQuerySet):
    def basic_contact(self):
        cc = CustomerContact.objects.filter(customer=OuterRef("pk")).filter(
            is_basic=True
        )
        return self.annotate(basic_contact_id=Subquery(cc.values("contact_id")[:1]))


class Customer(BaseResourceModel):
    """
    所有者ID    土地所有者名    土地所有者住所	連絡先情報  口座情報	タグ
    """

    name_kanji = JSONField(default=DefaultCustomer.name_kanji, db_index=True)
    name_kana = JSONField(default=DefaultCustomer.name_kana, db_index=True)
    address = JSONField(default=DefaultCustomer.address, db_index=True)
    banking = JSONField(default=DefaultCustomer.banking)
    tags = JSONField(default=dict)

    objects = CustomerQueryset.as_manager()


class Contact(BaseResourceModel):
    contact_info = JSONField(
        default=DefaultContact.contact_info
    )  # TODO: keep for migration, will drop later

    name_kanji = JSONField(default=DefaultCustomer.name_kanji, db_index=True)
    name_kana = JSONField(default=DefaultCustomer.name_kana, db_index=True)
    address = JSONField(default=DefaultCustomer.address, db_index=True)
    postal_code = models.CharField(default=None, max_length=200, null=True)
    telephone = models.CharField(default=None, max_length=200, null=True)
    mobilephone = models.CharField(default=None, max_length=200, null=True)
    email = models.EmailField(default=None, max_length=200, null=True)
