import logging

from django.db.models import Value
from django.db.models.functions import Concat
from django.db.models.signals import post_save
from django.dispatch import receiver

from hyakumori_crm.crm.models import Archive, Customer
from hyakumori_crm.users.models import User


def refresh_user_participants_cache(archive: Archive, save=False):
    archive.attributes["user_cache"] = dict(
        count=archive.archiveuser_set.count(),
        list=list(
            archive
                .archiveuser_set.all()
                .annotate(full_name=Concat("user__last_name", Value(" "), "user__first_name"))
                .values("user_id", "full_name")))
    if save:
        archive.save()

    return archive


def refresh_forest_cache(archive: Archive, save=False):
    archive.attributes["forest_cache"] = dict(
        count=archive.archiveforest_set.count(),
        list=list(
            archive
                .archiveforest_set.all()
                .values("forest__internal_id")))
    if save:
        archive.save()

    return archive


def refresh_customers_cache(archive: Archive, save=False):
    archive.attributes["customer_cache"] = dict(
        count=archive.archivecustomer_set.count(),
        list=list(
            archive.archivecustomer_set.all().values(
                "customer__id", "customer__name_kanji", "customer__name_kana", )))
    if save:
        archive.save()

    return archive


def refresh_single_archive_cache(archive: Archive):
    refresh_customers_cache(archive, save=False)
    refresh_user_participants_cache(archive, save=False)
    refresh_forest_cache(archive, save=False)
    archive.save(update_fields=["attributes", "updated_at"])
    return archive


@receiver(post_save, sender=Customer)
def update_customer_cache(sender, instance, created, **kwargs):
    if not created:
        try:
            for archivecustomer in instance.archivecustomer_set.iterator():
                refresh_customers_cache(archivecustomer.archive, save=True)
        except:
            logging.warning(f"could not refresh customer cache for archive {instance.pk}")
            pass


@receiver(post_save, sender=User)
def update_user_cache(sender, instance, created, **kwargs):
    if not created:
        try:
            for archiveuser in instance.archiveuser_set.iterator():
                refresh_user_participants_cache(archiveuser.archive, save=True)
        except:
            logging.warning(f"could not refresh user cache for archive {instance.pk}")
            pass
