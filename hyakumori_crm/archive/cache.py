from django.db.models import Value
from django.db.models.functions import Concat

from hyakumori_crm.crm.models import Archive


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
                "customer__id", "customer__name_kanji", "customer__name_kana",)))
    if save:
        archive.save()

    return archive

