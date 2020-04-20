from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_typed_views import typed_action

from hyakumori_crm.core.utils import default_paginator
from hyakumori_crm.crm.models import Contact, Customer, ForestCustomer
from hyakumori_crm.crm.restful.serializers import ContactSerializer, CustomerSerializer

from .schemas import ForestSerializer
from .service import (
    get_customer_contacts,
    get_customer_forest_relations,
    contacts_list_with_search,
)


class CustomerViewSets(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.all()

    @typed_action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def contacts(self, request):
        obj = self.get_object()

        paginator = default_paginator()
        paged_list = paginator.paginate_queryset(
            request=request, queryset=get_customer_contacts(obj.pk), view=self,
        )

        contacts = ContactSerializer(paged_list, many=True)
        return paginator.get_paginated_response(contacts.data)

    @typed_action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def forests(self, request):
        obj = self.get_object()

        paginator = default_paginator()
        paged_list = paginator.paginate_queryset(
            request=request, queryset=get_customer_forest_relations(obj.pk), view=self,
        )

        forests = []
        for forest_customer in paged_list:
            _forest = ForestSerializer(forest_customer.forest).data
            _contact = ContactSerializer(forest_customer.contact).data
            _forest["contact"] = _contact
            forests.append(_forest)

        return paginator.get_paginated_response(forests)

    @typed_action(detail=True, methods=["GET"])
    def representatives(self, request):
        return Response()

    @typed_action(detail=True, methods=["GET"])
    def related_archives(self, request):
        return Response()


@api_view(["GET"])
def contacts_list(request):
    paginator = default_paginator()
    paged_list = paginator.paginate_queryset(
        request=request, queryset=contacts_list_with_search(request.GET.get("search"))
    )
    return paginator.get_paginated_response(
        ContactSerializer(paged_list, many=True).data
    )
