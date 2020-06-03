from rest_framework.request import Request
from rest_typed_views import CurrentUser

from hyakumori_crm.users.models import User
from .enums import SystemGroups
from .services import PermissionService
from ..api.decorators import typed_api_view
from ..core.utils import make_success_json


@typed_api_view(["GET"])
def get_resource_permissions(
    request: Request, user: User = CurrentUser(member_of=SystemGroups.GROUP_ADMIN)
):
    permissions = PermissionService.get_app_permissions(app_label="crm")
    return make_success_json(data=dict(permissions=permissions))


@typed_api_view(["GET"])
def get_groups(
    request: Request, user: User = CurrentUser(member_of=SystemGroups.GROUP_ADMIN)
):
    groups = PermissionService.get_groups()
    return make_success_json(data=dict(groups=groups))
