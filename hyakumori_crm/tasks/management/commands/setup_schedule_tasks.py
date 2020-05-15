from distutils.util import strtobool

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django_q.tasks import schedule

from hyakumori_crm.permissions.services import PermissionService
from hyakumori_crm.activity.services import ActivityService
from hyakumori_crm.tags.services import TagService


class Command(BaseCommand):
    help = "Setup schedule tasks"

    def handle(self, *args, **kwargs):
        schedule('hyakumori_crm.tasks.healthcheck.do_healthcheck',
                 schedule_type=Schedule.MINUTES,
                 minutes=1)



