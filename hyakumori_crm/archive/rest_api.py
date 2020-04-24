import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser

from hyakumori_crm.crm.models import Archive, Attachment, Customer, Forest, ArchiveCustomer, ArchiveForest
from hyakumori_crm.crm.restful.serializers import ArchiveSerializer, ArchiveCustomerSerializer, AttachmentSerializer, ContactSerializer
from hyakumori_crm.users.serializers import UserSerializer
from .service import ArchiveService


class ArchiveCreateApi(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = ArchiveSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return Archive.objects.all()

    def post(self, request, model=None, model_pk=None, format=None):
        validated_data = dict()

        validated_data['consult_date'] = request.data['consult_date']
        validated_data['location'] = json.loads(request.data['location'])
        validated_data['attributes'] = json.loads(request.data['attributes'])
        validated_data['discuss_content'] = request.data['discuss_content']
        validated_data['future_action'] = request.data['future_action']
        validated_data['file_upload_list'] = request.FILES

        validated_data['customer_id_set'] = set(request.data['customer_ids'].split(','))
        validated_data['forest_id_set'] = set(request.data['forest_ids'].split(','))
        if model:
            if model == 'customers':
                validated_data['customer_id_set'].add(model_pk)
            if model == 'forests':
                validated_data['forest_id_set'].add(model_pk)

        validated_data['creator'] = request.user
        archive_service = ArchiveService()
        archive_created = archive_service.create_archive(validated_data)
        return Response(status=HTTP_200_OK, data=self.serializer_class(archive_created).data)


class ArchiveDetailApi(APIView):

    serializer_class = ArchiveSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self, pk):
        return Archive.objects.get(pk=pk)

    def get(self, request, pk=None):

        archive_detail = self.get_object(pk)

        archive_serializer = self.serializer_class(archive_detail)

        return Response(archive_serializer.data)

    def put(self, request, pk, format=None):
        pass


class ArchiveFileUploadApi(APIView):
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = [IsAuthenticated, ]

    def get_object(self, pk):
        return Archive.objects.get(pk=pk)

    def post(self, request, pk, *args, **kwargs):
        archive_detail = self.get_object(pk)
        file_upload_list = request.FILES
        for file_upload in file_upload_list:
            attachment_model = Attachment()
            attachment_model.content_object = archive_detail
            attachment_model.attachment_file = file_upload_list[file_upload]
            attachment_model.creator = request.user
            attachment_model.save()

        return Response(status=HTTP_200_OK, data=ArchiveSerializer(archive_detail).data)


class ArchiveCustomerActionApi(APIView):
    parser_classes = [JSONParser,]
    permission_classes = [IsAuthenticated, ]

    def get_object(self, pk):
        return Archive.objects.get(pk=pk)

    def put(self, request, pk):

        archive_service = ArchiveService(self.get_object(pk))
        customer_id_list = request.data['customer_id_list']

        if customer_id_list:

            validated_data = {'customer_id_add_list' : [customer_id_list[id_key] for id_key in customer_id_list]}
            archive_update = archive_service.update(validated_data)
            return Response(status=HTTP_200_OK, data=ArchiveSerializer(archive_update).data)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        archive_service = ArchiveService(self.get_object(pk))

        customer_id_del_list = request.data

        if customer_id_del_list:
            validated_data = {'customers_delete': [customer_id_del_list[id_key] for id_key in customer_id_del_list]}
            archive_update = archive_service.update(validated_data)
            return Response(status=HTTP_200_OK, data=ArchiveSerializer(archive_update).data)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class ArchiveCustomerContactActionApi(APIView):
    parser_classes = [JSONParser, FormParser]
    permission_classes = [IsAuthenticated, ]

    def get_object(self, pk):
        return Archive.objects.get(pk=pk)

    def get(self, request, pk, customer_id, add_flag=None):

        archive_service = ArchiveService(self.get_object(pk))

        if add_flag == 1:
            contact_set = archive_service.get_contact_list_can_add(customer_id)
        else:
            contact_set = archive_service.get_contacts_added_for_archive_customer(customer_id)

        contact_serializer_list = ContactSerializer(contact_set, many=True)
        return Response(status=HTTP_200_OK, data=contact_serializer_list.data)

    def put(self, request, pk, customer_id, add_flag=None):

        archive_service = ArchiveService(self.get_object(pk))

        contact_id_set = request.data['contact_id_list']
        archive_service.add_contact_to_archive_customer(customer_id, contact_id_set)

        return Response(status=HTTP_200_OK)

    def delete(self, request, pk, customer_id, add_flag=None):

        archive_service = ArchiveService(self.get_object(pk))

        contact_id_list = request.data['contact_id_list']
        archive_service.delete_contact_for_archive_customer(customer_id, contact_id_list)

        return Response(status=HTTP_200_OK)


class ArchiveForestActionApi(APIView):
    parser_classes = [JSONParser,]
    permission_classes = [IsAuthenticated, ]

    def get_object(self, pk):
        return Archive.objects.get(pk=pk)

    def put(self, request, pk, format=None):
        archive_service = ArchiveService(self.get_object(pk))

        forest_id_list = request.data

        if forest_id_list:

            validated_data = {'forest_id_add_list' : [forest_id_list[id_key] for id_key in forest_id_list]}
            archive_update = archive_service.update(validated_data)
            return Response(status=HTTP_200_OK, data=ArchiveSerializer(archive_update).data)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        archive_service = ArchiveService(self.get_object(pk))
        forest_id_list = request.data

        if forest_id_list:
            validated_data = {'forest_ids_delete_list': [forest_id_list[id_key] for id_key in forest_id_list]}
            archive_update = archive_service.update(validated_data)
            return Response(status=HTTP_200_OK, data=ArchiveSerializer(archive_update).data)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
