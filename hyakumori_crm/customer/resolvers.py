import uuid

from ariadne import ObjectType
from django.utils.translation import gettext as _t

from ..core.decorators import validate_model
from .schemas import (
    CustomerInputSchema,
    CustomerRead,
    CustomerUpdate,
    CustomerFilter,
    CustomerPaginator,
)
from .service import create, get, get_list, update

query = ObjectType("Query")
mutation = ObjectType("Mutation")


@query.field("get_customer")
def get_customer_by_id(_, info, id: str = None) -> dict:
    return {
        "ok": True,
        "customer": {
            "id": uuid.uuid4(),
            "internal_id": "ajshdq8w123",
            "profile": {"first_name": "Ha", "last_name": "Tran", "middle_name": None},
            "attributes": None,
        },
    }


@query.field("customertable_headers")
def get_customertable_headers(_, info) -> dict:
    headers = [
        {"text": _t("Internal Id"), "value": "internal_id"},
        {"text": _t("Fullname Kanji"), "value": "fullname_kanji"},
        {"text": _t("Fullname Kana"), "value": "fullname_kana"},
        {"text": _t("Postal Code"), "value": "postal_code"},
        {"text": _t("Address"), "value": "address"},
        {"text": _t("Prefecture"), "value": "prefecture"},
        {"text": _t("Municipality"), "value": "municipality"},
        {"text": _t("Ranking"), "value": "ranking"},
        {"text": _t("Status"), "value": "status"},
        {"text": _t("Telephone"), "value": "telephone"},
        {"text": _t("Mobilephone"), "value": "mobilephone"},
        {"text": _t("Email"), "value": "email"},
        {"text": _t("Representative"), "value": "representative"},
    ]
    filters = CustomerFilter.get_filters()
    for header_define in headers:
        if header_define["value"] in filters:
            _filter = filters[header_define["value"]]
            header_define["filter_name"] = header_define["value"]

    return {"ok": True, "headers": headers}


@query.field("list_customers")
@validate_model(CustomerPaginator)
def list_customers(_, info, data=None) -> dict:
    pager_input = data.dict()
    customers, total = get_list(
        page_num=pager_input["page_num"],
        per_page=pager_input["per_page"],
        pre_per_page=pager_input["pre_per_page"],
        order_by=pager_input["order_by"],
        filters=pager_input["filters"],
    )
    return {"items": customers, "total": total}


@mutation.field("create_customer")
@validate_model(CustomerInputSchema)
def create_customer(_, info, data=None) -> dict:
    customer = create(data)
    return {"customer": {"id": customer.id}}


@mutation.field("update_customer")
@validate_model(CustomerUpdate, get)
def update_customer(_, info, instance=None, data=None) -> dict:
    instance = update(instance, data)
    return {"customer": {"id": instance.id}}


resolvers = [query, mutation]
