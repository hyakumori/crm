from django.core.management.base import BaseCommand
from sequences.models import Sequence

from hyakumori_crm.crm.common.constants import CUSTOMER_ID_PREFIX, CUSTOMER_ID_SEQUENCE
from hyakumori_crm.crm.common.utils import generate_sequential_id
from hyakumori_crm.crm.models import Customer


class Command(BaseCommand):
    help = "Generate customer ids"

    def add_arguments(self, parser):
        parser.add_argument(
            "--recreate",
            dest="recreate",
            action="store_true",
            help="recreate all ids even existed, reset from 0",
        )
        parser.add_argument(
            "--no-recreate",
            dest="recreate",
            action="store_false",
            help="disable recreate, only insert for empty value",
        )
        parser.set_defaults(recreate=False)

    def handle(self, *args, **kwargs):
        recreate = kwargs.get("recreate")
        if recreate:
            Sequence.objects.filter(name=CUSTOMER_ID_SEQUENCE).update(last=0)
        qs = Customer.objects.order_by(
            "name_kanji__last_name", "name_kanji__first_name"
        )
        for customer in qs.iterator():
            if not customer.business_id or len(customer.business_id) == 0 or recreate:
                customer.business_id = generate_sequential_id(
                    CUSTOMER_ID_PREFIX, CUSTOMER_ID_SEQUENCE
                )
                customer.save()
                self.stdout.write(customer.business_id)

        self.stdout.write("DONE")
