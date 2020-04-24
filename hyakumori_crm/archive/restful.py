from django.http import Http404
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .service import *
from ..crm.restful.serializers import AttachmentSerialize


@api_view(["GET", "POST"])
def archives(req):
    if req.method == 'GET':
        return Response({"data": "get_list"})
    else:
        return Response({"data": "post"})


@api_view(["PUT", "PATCH", "DELETE"])
def archive(req, pk):
    if req.method == 'GET':
        return Response({"data": "get id"})
    elif req.method == 'DELETE':
        return Response({"data": "delete"})
    else:
        return Response({"data": "delete"})


@parser_classes([MultiPartParser])
@api_view(["GET", "POST"])
def attachments(req, archive_pk):
    # get list attachments
    if req.method == 'GET':
        try:
            attachments = get_all_attachments_by_archive_pk(archive_pk)
            return Response(data=AttachmentSerialize(attachments).data)
        except Attachment.DoesNotExist:
            raise Http404()
    else:
        try:
            archive = get_archive_by_pk(archive_pk)
            try:
                new_attachment = create_attachment(archive, data=req.FILES)
                return Response(data=AttachmentSerialize(new_attachment).data)
            except ValueError as err:
                raise Http404()
        except ValueError as err:
            raise Http404()


@api_view(["PUT", "PATCH", "DELETE"])
def attachment(req, archive_pk, attachment_pk):
    if req.method == 'DELETE':
        is_deleted = delete_attachment_file(archive_pk, attachment_pk)
        if is_deleted:
            return Response({"msg": "deleted"})
        else:
            raise Http404()
    else:
        print('Do put/patch')
