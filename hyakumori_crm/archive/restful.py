from django.http import Http404
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .service import *
from ..core.utils import default_paginator
from ..crm.restful.serializers import AttachmentSerialize, ArchiveSerializer, ForestSerializer, CustomerSerializer


@api_view(["GET", "POST"])
def archives(req):
    if req.method == 'GET':
        paginator = default_paginator()
        paged_list = paginator.paginate_queryset(
            request=req,
            queryset=Archive.objects.all()
        )
        return paginator.get_paginated_response(ArchiveSerializer(paged_list, many=True).data)
    else:
        try:
            archive = create_archive(req.data)
            if archive:
                return Response(data=ArchiveSerializer(archive).data)
            else:
                return Response({"msg": "No permission"})
        except ValueError:
            raise Http404()


@api_view(["GET", "PUT", "PATCH"])
def archive(req, pk):
    if req.method == 'GET':
        try:
            archive = get_archive_by_pk(pk)
            return Response({"data": ArchiveSerializer(archive).data})
        except ValueError:
            raise Http404()
    else:
        updated_archive = edit_archive(pk, req.data)
        return Response({"data": ArchiveSerializer(updated_archive).data})


@parser_classes([MultiPartParser])
@api_view(["GET", "POST"])
def attachments(req, archive_pk):
    # get list attachments
    if req.method == 'GET':
        try:
            Archive.objects.get(pk=archive_pk)
            attachments = get_all_attachments_by_archive_pk(archive_pk)
            return Response({"data": AttachmentSerialize(attachments, many=True).data})
        except Archive.DoesNotExist:
            raise Http404()
    else:
        try:
            archive = get_archive_by_pk(archive_pk)
            new_attachment = create_attachment(archive, req)
            return Response({"data": AttachmentSerialize(new_attachment, many=True).data})
        except ValueError:
            raise Http404()


@api_view(["DELETE"])
def attachment(req, archive_pk, attachment_pk):
    try:
        Archive.objects.get(pk=archive_pk)
        try:
            Attachment.objects.get(pk=attachment_pk)
            is_deleted = delete_attachment_file(archive_pk, attachment_pk)
            if is_deleted:
                return Response({"msg": "OK"})
            else:
                raise Http404()
        except Attachment.DoesNotExist:
            raise Http404()
    except Archive.DoesNotExist:
        raise Http404()


@api_view(["GET", "POST", "DELETE"])
def archive_forests(req, pk):
    if req.method == 'GET':
        forests = get_related_forests(pk)
        return Response({"data": ForestSerializer(forests, many=True).data})
    elif req.method == 'POST':
        try:
            forests = add_related_forest(pk, req.data)
            return Response({"data": ForestSerializer(forests, many=True).data})
        except ValueError:
            raise Http404()
    else:
        try:
            is_deleted = delete_related_forest(pk, req.data)
            if is_deleted:
                return Response({"msg": "OK"})
            else:
                raise Http404()
        except ValueError:
            raise Http404()


@api_view(["GET", "POST", "DELETE"])
def archive_customers(req, pk):
    if req.method == 'GET':
        customers = get_related_customer(pk)
        return Response({"data": CustomerSerializer(customers, many=True).data})
    elif req.method == 'POST':
        try:
            customers = add_related_customer(pk, req.data)
            return Response({"data": CustomerSerializer(customers, many=True).data})
        except ValueError:
            raise Http404()
    else:
        try:
            is_deleted = delete_related_customer(pk, req.data)
            if is_deleted:
                return Response({"msg": "OK"})
            else:
                raise Http404()
        except ValueError:
            raise Http404()
