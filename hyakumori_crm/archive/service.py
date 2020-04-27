from datetime import datetime

from django.utils.translation import gettext_lazy as _
from pydantic import ValidationError

from hyakumori_crm.crm.models import Archive, Attachment
from ..crm.models.customer import Customer
from ..crm.models.forest import Forest
from ..crm.models.relations import ArchiveUser, ArchiveForest, ArchiveCustomer
from ..customer.service import get_customer_by_pk
from ..forest.service import get_forest_by_pk


def get_archive_by_pk(pk):
    try:
        return Archive.objects.get(pk=pk)
    except(Archive.DoesNotExist, ValidationError):
        raise ValueError("Archive not found")


def get_attachment_by_pk(attachment_pk):
    try:
        return Attachment.objects.get(pk=attachment_pk)
    except Attachment.DoesNotExist:
        raise ValueError(_("Attachment not found"))


def get_all_attachments_by_archive_pk(archive_pk):
    return Attachment.objects.filter(object_id=archive_pk)


def get_attachment(archive_pk, attachment_pk):
    try:
        return Attachment.objects.filter(object_id=archive_pk, id=attachment_pk, deleted=None)
    except(Attachment.DoesNotExist, ValidationError):
        return ValueError(_("Attachment not found"))


def create_archive(author, data):
    archive = Archive()
    archive_user = ArchiveUser()
    archive_user.user_id = author.id
    archive_user.archive_id = archive.id
    archive.title = data.title
    archive.content = data.content
    archive.location = data.location
    archive.future_response = data.future_response
    archive.archive_date = datetime.now()
    archive.save()
    archive_user.save()
    return archive


def edit_archive(data):
    archive = data["archive"]
    archive.title = data["title"]
    archive.content = data["content"]
    archive.location = data["location"]
    archive.future_response = data["future_response"]
    archive.archive_date = data["archive_date"]
    archive.save()
    return archive


def create_attachment(archive, req):
    files = req.FILES.getlist("file")
    creator = req.user
    attachments = []
    for file in files:
        attachment = Attachment()
        attachment.creator = creator
        attachment.content_object = archive
        attachment.attachment_file = file
        attachment.save()
        attachments.append(attachment)
    return attachments


def delete_attachment_file(archive, attachment):
    try:
        attachment = get_attachment(archive.id, attachment.id)
        attachment.delete()
        return True
    except Attachment.DoesNotExist:
        return False


def get_related_forests(archive):
    return Forest.objects.filter(archiveforest__archive__id=archive.id, archiveforest__deleted=None)


def is_forest_exist(archive_pk, forest_pk):
    archive_forest = ArchiveForest.objects.filter(archive__id=archive_pk, forest__id=forest_pk, deleted=None)
    return True if len(archive_forest) == 1 else False


def add_related_forest(archive, data):
    forest_id_list = set(data.get("ids"))
    forests = []
    if forest_id_list and len(forest_id_list) > 0:
        for forest_id in forest_id_list:
            forest = get_forest_by_pk(forest_id)
            if is_forest_exist(archive.id, forest_id):
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


def delete_related_forest(archive, data):
    forest_id_list = set(data.get("ids"))
    if forest_id_list and len(forest_id_list) > 0:
        for forest_id in forest_id_list:
            forest = get_forest_by_pk(forest_id)
            if is_forest_exist(archive.id, forest_id):
                archive_forest = ArchiveForest.objects.get(archive_id=archive.id, forest_id=forest.id, deleted=None)
                archive_forest.delete()
            else:
                continue
        return True
    else:
        return False


def is_customer_exist(archive_pk, customer_pk):
    archive_customer = ArchiveCustomer.objects.filter(archive__id=archive_pk, customer__id=customer_pk, deleted=None)
    return True if len(archive_customer) == 1 else False


def get_related_customer(archive):
    return Customer.objects.filter(archivecustomer__archive__id=archive.id, archivecustomer__deleted=None)


def add_related_customer(archive, data):
    customer_id_list = set(data.get("ids"))
    customers = []
    if customer_id_list and len(customer_id_list) > 0:
        for customer_id in customer_id_list:
            customer = get_customer_by_pk(customer_id)
            if is_customer_exist(archive.id, customer_id):
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


def delete_related_customer(archive, data):
    customer_id_list = set(data.get("ids"))
    if customer_id_list and len(customer_id_list) > 0:
        for customer_id in customer_id_list:
            customer = get_customer_by_pk(customer_id)
            if is_customer_exist(archive.id, customer_id):
                archive_customer = ArchiveCustomer.objects.get(archive_id=archive.id, customer_id=customer.id,
                                                               deleted=None)
                archive_customer.delete()
            else:
                continue
        return True
    else:
        return False
