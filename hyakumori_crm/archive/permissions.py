from rest_framework.permissions import BasePermission
from hyakumori_crm.users.backends import HyakumoriBackend


class ChangeArchivePersmission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perms(["crm.change_archive"])
