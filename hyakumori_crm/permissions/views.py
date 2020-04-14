from django.contrib.auth.models import Group
from rest_framework.request import Request
from rest_framework.response import Response
from rest_typed_views import typed_api_view, CurrentUser

from hyakumori_crm.core.utils import model_to_dict
from hyakumori_crm.permissions.services import PermissionService
from hyakumori_crm.users.models import User


@typed_api_view(["GET"])
def get_resource_permissions(
    request: Request, user: User = CurrentUser(member_of="admin")
):
    permissions = PermissionService.get_app_permissions(app_label="crm")
    return Response(permissions)


@typed_api_view(["POST"])
def setup_groups(request: Request, user: User = CurrentUser()):
    # create admin group
    if user.is_superuser:
        admin_group, _ = Group.objects.get_or_create(name="admin")
        admin_group.user_set.add(user)
        admin_group.save()

    # create member group
    member_group, _ = Group.objects.get_or_create(name="member")

    # create normaluser group
    normal_user_group, _ = Group.objects.get_or_create(name="normal_user")

    groups = [model_to_dict(group) for group in Group.objects.all().iterator()]
    return Response(groups)
