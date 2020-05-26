from django.core.management.base import BaseCommand
from django_q.models import Schedule

from ...schedule import create_schedule


class Command(BaseCommand):
    help = "Setup schedule tasks"

    def handle(self, *args, **kwargs):
        create_schedule(
            func="hyakumori_crm.tasks.healthcheck.do_healthcheck",
            name="do_healthcheck",
            schedule_type=Schedule.MINUTES,
            minutes=1,
        )
