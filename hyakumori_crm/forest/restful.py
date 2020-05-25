import csv
import itertools

from django.db.models import Q, F, Count
from django.http import HttpResponse
from django.utils.translation import gettext as _
from rest_framework import mixins
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from hyakumori_crm.core.utils import default_paginator
from hyakumori_crm.crm.models import Forest, Archive
from hyakumori_crm.crm.restful.serializers import (
    CustomerSerializer,
    ForestSerializer,
    ContactSerializer,
    ArchiveSerializer, ForestListingSerializer,
)
from .schemas import (
    ForestInput,
    OwnerPksInput,
    CustomerDefaultInput,
    CustomerContactDefaultInput,
    ForestMemoInput,
)
from .service import (
    get_forest_by_pk,
    update,
    update_owners,
    get_forest_customers,
    get_customer_contacts_of_forest,
    set_default_customer,
    set_default_customer_contact,
    update_forest_memo, forest_csv_data_mapping,
    get_forests_for_csv, get_forests_by_ids, update_forest_tags, )
from ..activity.services import ActivityService, ForestActions
from ..api.decorators import (
    api_validate_model,
    get_or_404,
    action_login_required,
)
from ..crm.common.constants import (
    FOREST_CADASTRAL, FOREST_LAND_ATTRIBUTES, FOREST_OWNER_NAME, FOREST_CONTRACT, FOREST_ATTRIBUTES
)
from ..permissions.services import PermissionService


class ForestViewSets(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = ForestSerializer

    def get_queryset(self):
        if PermissionService.check_permissions(
            self.request, self.request.user, ["view_forest"]
        ):
            return Forest.objects.all()
        else:
            return Forest.objects.none()

    @action(["GET"], detail=False, url_path="minimal")
    @action_login_required(with_permissions=["view_forest"])
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
    @action_login_required(with_permissions=["view_customer"], is_detail=False)
    def customers(self, request, **kwargs):
        obj = self.get_object()

        paginator = default_paginator()
        paged_list = paginator.paginate_queryset(
            request=request, queryset=get_forest_customers(obj.pk), view=self,
        )

        return paginator.get_paginated_response(
            CustomerSerializer(paged_list, many=True).data
        )

    @action(["GET"], detail=True, url_path="archives")
    @get_or_404(
        get_func=get_forest_by_pk, to_name="forest", remove=True, pass_to="kwargs"
    )
    def archives(self, request, forest: Forest = None):
        archives = Archive.objects.filter(archiveforest__forest_id=forest.id)
        return Response(ArchiveSerializer(archives, many=True).data)

    @action(detail=True, methods=["PUT", "PATCH"], url_path="basic-info")
    @get_or_404(get_func=get_forest_by_pk, to_name="forest", remove=True)
    @api_validate_model(ForestInput, "forest_in")
    @action_login_required(with_permissions=["change_forest"])
    def basic_info(self, request, *, forest_in: ForestInput):
        update(forest_in.forest, forest_in.dict())
        ActivityService.log(
            ForestActions.basic_info_updated, forest_in.forest, request=request
        )
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

    @action(detail=True, methods=["POST"], url_path="memo")
    @get_or_404(
        get_func=get_forest_by_pk, to_name="forest", remove=True,
    )
    @api_validate_model(ForestMemoInput)
    @action_login_required(with_permissions=["change_forest"])
    def update_memo(self, request, *, data: ForestMemoInput = None):
        forest, updated = update_forest_memo(data.forest, data.memo)
        if updated:
            ActivityService.log(
                ForestActions.memo_info_updated, data.forest, request=request
            )
        return Response({"memo": forest.attributes["memo"]})

    @action(detail=False, methods=["GET", "POST"], url_path="download-csv")
    @action_login_required(with_permissions=["change_forest"])
    def download_all_csv(self, request):
        if request.data is None or len(request.data) == 0:
            csv_data = get_forests_for_csv()
        else:
            csv_data = get_forests_for_csv(request.data)
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment'
        header = ["\ufeff内部ID", "土地管理ID"]
        flatten_header = list(itertools.chain(header, FOREST_CADASTRAL, FOREST_LAND_ATTRIBUTES, FOREST_OWNER_NAME,
                                              FOREST_CONTRACT, [_("Tag")],
                                              FOREST_ATTRIBUTES))
        writer = csv.writer(response)
        writer.writerow(flatten_header)
        for forest in csv_data:
            csv_row = forest_csv_data_mapping(forest)
            writer.writerow(csv_row)
        return response

    @action(detail=False, methods=["PUT"], url_path="ids")
    @action_login_required(with_permissions=["change_forest"])
    def get_forests_by_ids(self, request):
        ids = request.data
        if ids is None or len(ids) == 0:
            return Response({"data": []})
        else:
            forests = get_forests_by_ids(ids)
            return Response(ForestListingSerializer(forests, many=True).data)

    @action(detail=False, methods=["PUT"], url_path="tags")
    @action_login_required(with_permissions=["change_forest"])
    def tags(self, request):
        update_forest_tags(request.data)
        return Response({"msg": "OK"})


@api_view(["PUT", "PATCH"])
@get_or_404(get_func=get_forest_by_pk, to_name="forest", remove=True)
@api_validate_model(OwnerPksInput, "owner_pks_in")
@action_login_required(with_permissions=["change_forest"])
def update_owners_view(request, *, owner_pks_in: OwnerPksInput):
    update_owners(owner_pks_in)
    ActivityService.log(
        ForestActions.customers_updated, owner_pks_in.forest, request=request
    )
    return Response({"id": owner_pks_in.forest.pk})


@api_view(["PUT", "PATCH"])
@get_or_404(get_forest_by_pk, to_name="forest", remove=True)
@api_validate_model(CustomerDefaultInput)
@action_login_required(with_permissions=["change_forest"])
def set_default_customer_view(request, *, data: CustomerDefaultInput = None):
    set_default_customer(data)
    ActivityService.log(ForestActions.customers_updated, data.forest, request=request)
    return Response({"id": data.forest.id})


@api_view(["PUT", "PATCH"])
@get_or_404(get_forest_by_pk, to_name="forest", remove=True)
@api_validate_model(CustomerContactDefaultInput)
@action_login_required(with_permissions=["change_forest"])
def set_default_customer_contact_view(
    request, *, data: CustomerContactDefaultInput = None
):
    set_default_customer_contact(data)
    ActivityService.log(ForestActions.customers_updated, data.forest, request=request)
    return Response({"id": data.forest.id})
