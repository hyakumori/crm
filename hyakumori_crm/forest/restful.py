from django.db.models import Q, F, Count
from rest_framework import mixins
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_typed_views import typed_action

from hyakumori_crm.core.utils import default_paginator
from hyakumori_crm.crm.models import Forest, Customer
from hyakumori_crm.crm.restful.serializers import (
    CustomerSerializer,
    ForestSerializer,
    ContactSerializer,
)
from ..api.decorators import (
    api_validate_model,
    get_or_404,
    action_login_required,
)
from .schemas import (
    ForestInput,
    OwnerPksInput,
    CustomerDefaultInput,
    CustomerContactDefaultInput,
)
from .service import (
    get_forest_by_pk,
    update,
    update_owners,
    get_customers,
    get_customer_contacts_of_forest,
    set_default_customer,
    set_default_customer_contact,
)
from ..permissions.services import PermissionService


class ForestViewSets(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = ForestSerializer

    def get_queryset(self):
        if PermissionService.check_permissions(self.request, self.request.user, ["view_customer"]):
            return Forest.objects.all()
        else:
            return Forest.objects.none()

    @action(["GET"], detail=False, url_path="minimal")
    @action_login_required(
        with_permissions=["view_forest"]
    )
    def list_minimal(self, request):
        query = (
            self.get_queryset()
            .annotate(customers_count=Count(F("forestcustomer__customer_id")))
            .values("id", "internal_id", "cadastral", "customers_count")
        )
        search_str = request.GET.get("search")
        if search_str:
            query = query.filter(
                Q(pk__icontains=search_str)
                | Q(internal_id__icontains=search_str)
                | Q(cadastral__prefecture__icontains=search_str)
                | Q(cadastral__municipality__icontains=search_str)
                | Q(cadastral__sector__icontains=search_str)
                | Q(cadastral__subsector__icontains=search_str)
            )

        paginator = default_paginator()
        paged_list = paginator.paginate_queryset(
            request=request, queryset=query, view=self
        )
        return paginator.get_paginated_response(paged_list)

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    @action_login_required(
        with_permissions=["view_customer"]
    )
    def customers(self, request, **kwargs):
        obj = self.get_object()

        paginator = default_paginator()
        paged_list = paginator.paginate_queryset(
            request=request, queryset=get_customers(obj.pk), view=self,
        )

        return paginator.get_paginated_response(
            CustomerSerializer(paged_list, many=True).data
        )

    @typed_action(detail=True, methods=["GET"])
    def related_archives(self, request):
        return Response()

    @action(detail=True, methods=["PUT", "PATCH"], url_path="basic-info")
    @get_or_404(get_func=get_forest_by_pk, to_name="forest", remove=True)
    @api_validate_model(ForestInput, "forest_in")
    @action_login_required(
        with_permissions=["change_forest"]
    )
    def basic_info(self, request, *, forest_in: ForestInput):
        update(forest_in.forest, forest_in.dict())
        return Response({"id": forest_in.forest.pk})

    @action(detail=True, methods=["GET"], url_path="customers-forest-contacts")
    @get_or_404(get_forest_by_pk, to_name="forest", pass_to="kwargs", remove=True)
    def customers_forest_contacts(self, request, *, forest: Forest):
        contacts = get_customer_contacts_of_forest(forest.pk)
        paginator = default_paginator()
        paged_list = paginator.paginate_queryset(
            request=request, queryset=contacts, view=self
        )
        return paginator.get_paginated_response(
            ContactSerializer(paged_list, many=True).data
        )


@api_view(["PUT", "PATCH"])
@get_or_404(get_func=get_forest_by_pk, to_name="forest", remove=True)
@api_validate_model(OwnerPksInput, "owner_pks_in")
@action_login_required(
    with_permissions=["change_customer"]
)
def update_owners_view(request, *, owner_pks_in: OwnerPksInput):
    update_owners(owner_pks_in)
    return Response({"id": owner_pks_in.forest.pk})


@api_view(["PUT", "PATCH"])
@get_or_404(get_forest_by_pk, to_name="forest", remove=True)
@api_validate_model(CustomerDefaultInput)
def set_default_customer_view(request, *, data: CustomerDefaultInput = None):
    set_default_customer(data)
    return Response({"id": data.forest.id})


@api_view(["PUT", "PATCH"])
@get_or_404(get_forest_by_pk, to_name="forest", remove=True)
@api_validate_model(CustomerContactDefaultInput)
def set_default_customer_contact_view(
    request, *, data: CustomerContactDefaultInput = None
):
    set_default_customer_contact(data)
    return Response({"id": data.forest.id})
