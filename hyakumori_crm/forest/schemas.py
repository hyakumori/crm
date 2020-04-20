from typing import Optional, List
from datetime import date
from uuid import UUID
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, CharFilter, DateFilter
from pydantic import validator, root_validator

from hyakumori_crm.core.models import HyakumoriDanticModel
from hyakumori_crm.crm.models import Contact
from hyakumori_crm.crm.schemas.contract import ContractType
from ..core.models import Paginator
from ..crm.models import Forest, ForestCustomer, Customer


class ForestFilter(FilterSet):
    internal_id = CharFilter(lookup_expr="icontains", method="icontains_filter")
    cadastral__prefecture = CharFilter(
        lookup_expr="icontains", method="icontains_filter"
    )
    cadastral__municipality = CharFilter(
        lookup_expr="icontains", method="icontains_filter"
    )
    cadastral__sector = CharFilter(lookup_expr="icontains", method="icontains_filter")
    cadastral__subsector = CharFilter(
        lookup_expr="icontains", method="icontains_filter"
    )
    owner__name_kana = CharFilter(lookup_expr="icontains", method="icontains_filter")
    owner__name_kanji = CharFilter(lookup_expr="icontains", method="icontains_filter")
    owner__address__prefecture = CharFilter(
        lookup_expr="icontains", method="icontains_filter"
    )
    owner__address__municipality = CharFilter(
        lookup_expr="icontains", method="icontains_filter"
    )
    owner__address__sector = CharFilter(
        lookup_expr="icontains", method="icontains_filter"
    )
    contracts__0__status = CharFilter(
        lookup_expr="icontains", method="icontains_filter"
    )
    contracts__0__start_date = DateFilter(method="exact_date_filter")
    contracts__0__end_date = DateFilter(method="exact_date_filter")
    contracts__1__status = CharFilter(
        lookup_expr="icontains", method="icontains_filter"
    )
    contracts__1__start_date = DateFilter(method="exact_date_filter")
    contracts__1__end_date = DateFilter(method="exact_date_filter")
    contracts__2__status = CharFilter(
        lookup_expr="icontains", method="icontains_filter"
    )
    contracts__2__start_date = DateFilter(method="exact_date_filter")
    contracts__2__end_date = DateFilter(method="exact_date_filter")
    tag__danchi = CharFilter(lookup_expr="icontains", method="icontains_filter")
    tag__manage_type = CharFilter(lookup_expr="icontains", method="icontains_filter")

    def icontains_filter(self, queryset, name, value):
        return queryset.filter(**{name + "__icontains": value})

    def exact_date_filter(self, queryset, name, value):
        return queryset.filter(**{name: value})

    class Meta:
        model = Forest
        fields = []


class ForestPaginator(Paginator):
    @validator("filters")
    def validate_filters(cls, filter_input):
        return ForestFilter(filter_input)


class Cadastral(HyakumoriDanticModel):
    prefecture: str
    municipality: str
    sector: str
    subsector: Optional[str]


class Contract(HyakumoriDanticModel):
    type: ContractType
    status: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]


class ForestInput(HyakumoriDanticModel):
    forest: Forest
    cadastral: Cadastral
    contracts: List[Contract]

    class Config:
        arbitrary_types_allowed = True


class OwnerPksInput(HyakumoriDanticModel):
    forest: Forest
    added: List[UUID] = []
    deleted: List[UUID] = []

    class Config:
        arbitrary_types_allowed = True

    @validator("deleted")
    def check_deleted(cls, v):
        owner_pks = ForestCustomer.objects.filter(customer_id__in=v).values_list(
            "customer_id"
        )
        invalid_pks = set(v) - set(owner_pks)
        if len(invalid_pks) > 0:
            v = list(invalid_pks)
            raise ValueError(_(f"Customer Id {v} not found"))
        return v

    @validator("added")
    def check_added(cls, v):
        owner_pks = Customer.objects.filter(id__in=v).values_list("id", flat=True)
        invalid_pks = set(v) - set(owner_pks)
        if len(invalid_pks) > 0:
            v = list(invalid_pks)
            raise ValueError(_(f"Customer Id {v} not found"))
        return v


class ForestOwnerContractInput(HyakumoriDanticModel):
    forest: Forest
    customer: Customer
    contact: Contact

    class Config:
        arbitrary_types_allowed = True

    @validator("contact", pre=True)
    def prepare_contact(cls, v):
        if not isinstance(v, Contact):
            try:
                return Contact.objects.get(pk=v)
            except (Contact.DoesNotExist, ValidationError):
                raise ValueError(_("Contact not found"))
        return v
