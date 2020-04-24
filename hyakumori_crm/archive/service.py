from pydantic import ValidationError

from hyakumori_crm.crm.models import Archive, Attachment


def get_archive_by_pk(pk):
    try:
        return Archive.objects.get(pk=pk)
    except(Archive.DoesNotExist, ValidationError):
        raise ValueError("Archive not found")


def get_all_attachments_by_archive_pk(archive_pk):
    return Attachment.objects.get(object_id=archive_pk)


def get_attachment(archive_pk, attachment_pk):
    try:
        return Attachment.objects.filter(object_id=archive_pk, id=attachment_pk)
    except(Attachment.DoesNotExist, ValidationError):
        return ValueError("Attachment not found")


def create_attachment(archive, data):
    print(data)
    files = data.getlist('file')
    attachments = []
    for file in files:
        attach = Attachment()
        attach.content_object = archive
        attach.attachment_file = file
        attachments.append(attach)
    return attachments


def delete_attachment_file(archive_pk, attachment_pk):
    try:
        attachment = get_attachment(archive_pk, attachment_pk)
        attachment.delete()
        return True
    except ValueError:
        return False
