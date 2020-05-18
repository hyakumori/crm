import logging
from typing import List

from hyakumori_crm.crm.common.utils import get_customer_name
from hyakumori_crm.crm.models import ForestCustomerContact
import time

logger = logging.Logger(__name__)


def refresh_customer_forest_cache(forest_ids: List[str]):
    filters = dict(customercontact__is_basic=True)
    if len(forest_ids) > 0:
        filters["forestcustomer__forest_id__in"] = forest_ids

    forestcustomercontacts = ForestCustomerContact.objects \
        .filter(**filters) \
        .select_related("customercontact__contact", "forestcustomer__customer", "forestcustomer__forest")

    now = time.time()

    for fcc in forestcustomercontacts.iterator():
        try:
            forest = fcc.forestcustomer.forest
            customer = fcc.forestcustomer.customer
            self_contact = fcc.customercontact.contact

            forest.refresh_from_db()
            if forest.attributes.get("customer_cache") is None:
                forest.attributes["customer_cache"] = dict(list=dict(), repr_name_kanji="", repr_name_kana="")

            _repr_name_kanji = []
            _repr_name_kana = []
            if isinstance(forest.attributes["customer_cache"]["list"], list):
                forest.attributes["customer_cache"]["list"] = {}

            customer_id = str(customer.id)
            if customer_id in forest.attributes["customer_cache"]["list"]:
                del forest.attributes["customer_cache"]["list"][customer_id]

            forest.attributes["customer_cache"]["list"][customer_id] = dict(
                contact_id=str(self_contact.id),
                name_kanji=self_contact.name_kanji,
                name_kana=self_contact.name_kana)

            for _, item in forest.attributes["customer_cache"]["list"].items():
                _repr_name_kanji.append(get_customer_name(item.get("name_kanji")))
                _repr_name_kana.append(get_customer_name(item.get("name_kana")))

            forest.attributes["customer_cache"]["repr_name_kanji"] = ",".join(_repr_name_kanji)
            forest.attributes["customer_cache"]["repr_name_kana"] = ",".join(_repr_name_kana)
            forest.save(update_fields=["attributes", "updated_at"])
        except Exception as e:
            logger.warning(
                f"could not saving latest user self contact info in forest: {fcc.forestcustomer.forest.pk}", exc_info=e
            )

    logger.info(f"Cache reloading has been finished, time cost: {time.time() - now}s")
