from django.utils.translation import gettext_lazy as _
from pydantic import ValidationError

from hyakumori_crm.crm.models import Archive, Attachment
from ..crm.models.customer import Customer
from ..crm.models.forest import Forest
from ..crm.models.relations import ArchiveUser, ArchiveForest, ArchiveCustomer
from ..customer.service import get_customer_by_pk
from ..forest.service import get_forest_by_pk
from ..permissions.services import PermissionService
from ..users.models import User


def get_archive_by_pk(pk):
    try:
        return Archive.objects.get(pk=pk)
    except(Archive.DoesNotExist, ValidationError):
        raise ValueError("Archive not found")


def get_attachment_by_pk(pk):
    try:
        return Attachment.objects.get(pk=pk)
    except Attachment.DoesNotExist:
        raise ValueError(_("Attachment not found"))


def get_all_attachments_by_archive_pk(archive_pk):
    return Attachment.objects.filter(object_id=archive_pk)


def get_attachment(archive_pk, attachment_pk):
    try:
        return Attachment.objects.filter(object_id=archive_pk, id=attachment_pk)
    except(Attachment.DoesNotExist, ValidationError):
        return ValueError(_("Attachment not found"))


def map_archive(archive, data):
    archive.title = data.get("title")
    archive.content = data.get("content")
    archive.location = data.get("location")
    archive.future_response = data.get("future_response")
    archive.archive_date = data.get("archive_date")
    archive.save()


def create_archive(data):
    try:
        user = User.objects.get(pk=data.get("author_id"))
        user_perms = PermissionService.get_user_permissions(user.id)
        if len(user_perms["groups"]) == 0:
            archive = Archive()
            archive_user = ArchiveUser()
            archive_user.user_id = user.id
            archive_user.archive_id = archive.id
            map_archive(archive, data)
            archive_user.save()
            return archive
        else:
            return None
    except User.DoesNotExist:
        raise ValueError(_("Creator not found"))


def edit_archive(pk, data):
    archive = get_archive_by_pk(pk)
    map_archive(archive, data)
    return archive


def create_attachment(archive, req):
    files = req.FILES.getlist("file")
    try:
        creator_id = req.data.get("creator")
        creator = User.objects.get(pk=creator_id)
        attachments = []
        for file in files:
            attachment = Attachment()
            attachment.creator = creator
            attachment.content_object = archive
            attachment.attachment_file = file
            attachment.save()
            attachments.append(attachment)
        return attachments
    except User.DoesNotExist:
        raise ValueError(_("Creator not found"))


def delete_attachment_file(archive_pk, attachment_pk):
    try:
        attachment = get_attachment(archive_pk, attachment_pk)
        attachment.delete()
        return True
    except Attachment.DoesNotExist:
        return False


def get_related_forests(archive_pk):
    return Forest.objects.filter(archiveforest__archive__id=archive_pk)


def is_forest_exist(archive_pk, forest_pk):
    archive_forest = ArchiveForest.objects.filter(archive__id=archive_pk, forest__id=forest_pk)
    return True if len(archive_forest) == 1 else False


def add_related_forest(archive_pk, data):
    archive = get_archive_by_pk(pk=archive_pk)
    forest_id_list = set(data.get("id"))
    forests = []
    if forest_id_list and len(forest_id_list) > 0:
        for forest_id in forest_id_list:
            forest = get_forest_by_pk(forest_id)
            if is_forest_exist(archive_pk, forest_id):
                forests.append(forest)
                continue
            else:
                archive_forest = ArchiveForest()
                archive_forest.archive_id = archive.id
                archive_forest.forest_id = forest.id
                archive_forest.save()
                forests.append(forest)
        return forests
    else:
        return None


def is_customer_exist(archive_pk, customer_pk):
    archive_customer = ArchiveCustomer.objects.filter(archive__id=archive_pk, customer__id=customer_pk)
    return True if len(archive_customer) == 1 else False


def get_related_customer(archive_pk):
    return Customer.objects.filter(archivecustomer__archive__id=archive_pk)


def add_related_customer(archive_pk, data):
    archive = get_archive_by_pk(pk=archive_pk)
    customer_id_list = set(data.get("id"))
    customers = []
    if customer_id_list and len(customer_id_list) > 0:
        for customer_id in customer_id_list:
            customer = get_customer_by_pk(customer_id)
            if is_customer_exist(archive_pk, customer_id):
                customers.append(customer)
            else:
                archive_customer = ArchiveCustomer()
                archive_customer.archive_id = archive.id
                archive_customer.customer_id = customer.id
                archive_customer.save()
                customers.append(customer)
        return customers
    else:
        return None
