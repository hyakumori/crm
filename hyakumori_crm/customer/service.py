from typing import Dict, Iterator, Union

from django.core.exceptions import ValidationError
from django.db.models import CharField, F, OuterRef, Subquery
from django.db.models import Value as V
from django.db.models.expressions import RawSQL
from django.db.models.functions import Concat


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
    # representatives = (
    #     Contact.objects.annotate(
    #         fullname=RawSQL(
    #             "concat(profile->>'last_name', ' ', profile->>'first_name')", [],
    #         )
    #     )
    #     .filter(customer=OuterRef("pk"))
    #     .order_by("-created_at")
    # )
    # query = (
    #     Customer.objects.annotate(
    #         fullname=RawSQL(
    #             "concat(profile->>'last_name', ' ', profile->>'first_name')", [],
    #         )
    #     )
    #     .annotate(phone=RawSQL("concat(profile->>'mobile_number')", []))
    #     .annotate(address=RawSQL("concat(profile->>'address')", []))
    #     .annotate(representative=Subquery(representatives.values("fullname")[:1]))
    #     .values("fullname", "phone", "address", "representative")
    # )
    # total = query.count()
    # customers = query.order_by(*order_by)[offset:per_page]
    # return customers, total
    return [], 0


def create(data):
    # customer = Customer(**data)
    # customer.save()
    # return customer
    pass


def update(customer, data):
    # do update...
    return customer
