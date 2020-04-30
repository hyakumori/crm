from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .constants import ArchiveActions, CustomerActions, ForestActions, UserActions
from .services import ActivityService
from ..core.utils import make_success_json
from ..crm.models.message_template import MessageTemplate


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_for_object(request, lang_code, app_label, object_type, object_id):
    results = ActivityService.get_log_for_object(lang_code, app_label, object_type, object_id)
    return Response(dict(results=results, count=len(results), next=None, previous=None))


@api_view(["POST"])
@permission_classes([IsAdminUser])
def setup_templates(request):
    MessageTemplate.objects.all().delete()

    ActivityService.import_message_templates(for_type="forest", action_class=ForestActions)
    ActivityService.import_message_templates(for_type="customer", action_class=CustomerActions)
    ActivityService.import_message_templates(for_type="archive", action_class=ArchiveActions)
    ActivityService.import_message_templates(for_type="user", action_class=UserActions)

    return make_success_json(data=dict(success=True))
