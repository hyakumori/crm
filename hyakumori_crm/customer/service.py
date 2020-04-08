from typing import Dict, Iterator, Union

from django.core.exceptions import ValidationError
from django.db.models import (
    Case,
    CharField,
    F,
    OuterRef,
    PositiveSmallIntegerField,
    Q,
    Subquery,
)
from django.db.models import Value as V
from django.db.models import When
from django.db.models.expressions import RawSQL
from django.db.models.functions import Concat
from querybuilder.query import Query

from hyakumori_crm.core.models import RawSQLField
from hyakumori_crm.crm.models.customer import Contact, Customer
from hyakumori_crm.crm.models.relations import CustomerContact
from hyakumori_crm.users.models import User

from .schemas import CustomerInputSchema


def get(pk):
    # try:
    #     return Customer.objects.get(pk=pk)
    # except (Customer.DoesNotExist, ValidationError):
    #     return None
    return None


def get_list(
    page_num: int = 1,
    per_page: int = 10,
    pre_per_page: Union[int, None] = None,
    order_by: Union[Iterator, None] = None,
):
    offset = (pre_per_page or per_page) * (page_num - 1)
    if not order_by:
        order_by = []

    representatives = (
        Query()
        .from_table(
            {"contact": Contact},
            [
                {
                    "fullname_kana": RawSQLField(
                        "concat(contact.name_kana->>'last_name', ' ', contact.name_kana->>'first_name')"
                    )
                }
            ],
        )
        .join({"cc": CustomerContact}, condition="contact.id = cc.contact_id",)
        .where("contact.customer_id = c.id")
        .order_by(RawSQLField("case when cc.attributes->>default then 1 else 2 end"))
    )

    query = (
        Query()
        .from_table(
            {"c": Customer},
            fields=[
                "internal_id",
                {"representative": RawSQLField(representatives.get_sql())},
            ],
        )
        .join(
            {"self_cc": CustomerContact},
            condition="c.id=self_cc.customer_id and self_cc.is_basic is true",
        )
        .join(
            {"self_contact": Contact},
            condition="self_cc.contact_id=self_contact.id",
            fields=[
                {
                    "fullname_kana": RawSQLField(
                        "concat(self_contact.name_kana->>'last_name', ' ', self_contact.name_kana->>'first_name')"
                    )
                },
                {
                    "fullname_kanji": RawSQLField(
                        "concat(self_contact.name_kanji->>'last_name', ' ', self_contact.name_kanji->>'first_name')"
                    )
                },
                "mobilephone",
                "telephone",
                "postal_code",
                {"address": "address->>'sector'"},
            ],
        )
    )
    return [], 0


def create(customer_in: CustomerInputSchema):
    admin = User.objects.filter(is_superuser=True, is_active=True).first()
    customer = Customer()
    customer.name_kanji = customer_in.name_kanji.dict()
    customer.name_kana = customer_in.name_kana.dict()
    customer.address = customer_in.address.dict()
    customer.status = customer_in.status
    customer.author = admin
    customer.editor = admin
    contacts = []
    customer_contacts = []

    self_contact = Contact(
        contact_info=customer_in.basic_contact.dict(), author=admin, editor=admin
    )
    contacts.append(self_contact)
    contact_rel = CustomerContact(
        customer=customer,
        contact=self_contact,
        is_basic=True,
        author=admin,
        editor=admin,
    )
    customer_contacts.append(contact_rel)

    if hasattr(customer_in, "contacts"):
        for data in customer_in.contacts:
            contact = Contact(contact_info=data.dict(), author=admin, editor=admin)
            contacts.append(contact)
            contact_rel = CustomerContact(
                customer=customer, contact=contact, author=admin, editor=admin
            )
            customer_contacts.append(contact_rel)
    customer.save()
    Contact.objects.bulk_create(contacts)
    CustomerContact.objects.bulk_create(customer_contacts)
    return customer


def update(customer, data):
    # do update...
    return customer
