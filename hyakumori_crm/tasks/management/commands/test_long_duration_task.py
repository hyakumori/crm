import os

from django.core.management.base import BaseCommand
from django_q.tasks import async_task
from django.conf import settings

class Command(BaseCommand):
    help = "Running a long time task"

    def handle(self, *args, **kwargs):
        BASE_DIR = settings.BASE_DIR
        task_id = async_task(
            func="hyakumori_crm.tasks.long_duration.process",
        )
        with open(os.join("BASE_DIR", task_id + ".task"), "w"):
            pass

