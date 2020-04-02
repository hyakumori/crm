from typing import Dict, Union, Iterator
from django.core.exceptions import ValidationError
from django.db.models import CharField, Value as V, F, OuterRef, Subquery
from django.db.models.functions import Concat
from django.db.models.expressions import RawSQL
from .models import Customer, Contact, CustomerContact


def get(pk):
    try:
        return Customer.objects.get(pk=pk)
    except (Customer.DoesNotExist, ValidationError):
        return None


def get_list(
    page_num: int = 1,
    per_page: int = 10,
    pre_per_page: Union[int, None] = None,
    sort_by: Union[Iterator, None] = None,
):
    assert per_page <= 100, "per_page must not be greater than 100"
    offset = (pre_per_page or per_page) * (page_num - 1)
    if not sort_by:
        sort_by = []
    representatives = (
        Contact.objects.annotate(
            fullname=RawSQL(
                "concat(profile->>'last_name', ' ', profile->>'first_name')", [],
            )
        )
        .filter(customer=OuterRef("pk"))
        .order_by("-created_at")
    )
    query = (
        Customer.objects.annotate(
            fullname=RawSQL(
                "concat(profile->>'last_name', ' ', profile->>'first_name')", [],
            )
        )
        .annotate(phone=RawSQL("concat(profile->>'mobile_number')", []))
        .annotate(address=RawSQL("concat(profile->>'address')", []))
        .annotate(representative=Subquery(representatives.values("fullname")[:1]))
        .values("fullname", "phone", "address", "representative")
    )
    total = query.count()
    customers = query.order_by(*sort_by)[offset:per_page]
    return customers, total


def create(data):
    customer = Customer(**data)
    customer.save()
    return customer


def add_contacts(customer, contact_data):
    contacts = []
    customer_contacts = []
    for data in contact_data:
        try:
            relationship_type = data.pop("relationship_type")
        except KeyError:
            relationship_type = ""
        contact = Contact(**data)
        contacts.append(contact)
        cc = CustomerContact(
            customer=customer, contact=contact, relationship_type=relationship_type
        )
        customer_contacts.append(cc)
    Contact.objects.bulk_create(contacts)
    CustomerContact.objects.bulk_create(customer_contacts)
    customer.save(update_fields=["updated_at"])
    return contacts


def update(customer, data):
    # do update...
    return customer
