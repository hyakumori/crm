from typing import List
from uuid import UUID

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, AbstractUser, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.module_loading import import_string

from guardian.shortcuts import (
    assign_perm,
    get_user_perms,
    remove_perm,
    get_objects_for_user,
)

from hyakumori_crm.core.utils import model_to_dict
from hyakumori_crm.permissions.enums import SystemGroups
from hyakumori_crm.permissions.serializers import GroupSerializer, PermissionSerializer


class PermissionService:
    @classmethod
    def serialize_groups(cls, qs):
        serializer = GroupSerializer(qs, many=True)
        return serializer.data

    @classmethod
    def get_app_permissions(cls, app_label, serialize=True):
        crm_content_types = (
            ContentType.objects.filter(app_label=app_label).all().values_list("id")
        )
        qs = Permission.objects.filter(content_type_id__in=crm_content_types).all()

        if serialize:
            permissions = PermissionSerializer(qs, many=True)
            return permissions.data

        return qs

    @classmethod
    def get_user_manage_resource(cls, user_id: UUID, app: str, resource_name: str):
        user = get_user_model().objects.get(pk=user_id)
        content_type = ContentType.objects.get(model=resource_name, app_label=app)
        if content_type:
            manage_code_name = f"crm.manage_{resource_name.lower()}"
            return get_objects_for_user(user, manage_code_name)
        else:
            raise Exception("ContentType not found")

    @classmethod
    def get_user_permissions(cls, user_id: UUID):
        user = get_user_model().objects.get(pk=user_id)
        user_groups = cls.serialize_groups(user.groups.all())
        results = dict(
            is_admin=user.is_superuser, is_staff=user.is_staff, groups=user_groups,
        )
        return results

    @classmethod
    def assign_user_to_group(
        cls, user_id: UUID, group_ids: List[int], clear: bool = True
    ):
        user = get_user_model().objects.get(pk=user_id)

        for group_id in group_ids:
            group = Group.objects.get(pk=group_id)
            if clear:
                user.groups.clear()
                user.save()
                group.refresh_from_db()

            group.user_set.add(user)
            group.save()

        return cls.serialize_groups(user.groups.all())

    @classmethod
    def unassign_user_from_group(cls, user_id: UUID, group_ids: List[int]):
        user = get_user_model().objects.get(pk=user_id)

        for group_id in group_ids:
            group = Group.objects.get(pk=group_id)
            group.user_set.remove(user)
            group.save()

        return cls.serialize_groups(user.groups.all())

    @classmethod
    def assign_object_permissions(
        cls, user_id: UUID, object_id: UUID, object_type_id, permission_ids: List[int]
    ):
        user = get_user_model().objects.get(pk=user_id)
        content_type = ContentType.objects.get_for_id(object_type_id)
        content_type_model = content_type.model_class()
        model_instance = content_type_model.objects.get(pk=object_id)

        for permission_id in permission_ids:
            permission = Permission.objects.get(pk=permission_id)
            assign_perm(permission.codename, user, model_instance)

        return get_user_perms(user, model_instance)

    @classmethod
    def unassign_object_permissions(
        cls, user_id: UUID, object_id: UUID, object_type_id, permission_ids: List[int]
    ):
        user = get_user_model().objects.get(pk=user_id)
        content_type = ContentType.objects.get_for_id(object_type_id)
        content_type_model = content_type.model_class()
        model_instance = content_type_model.objects.get(pk=object_id)

        for permission_id in permission_ids:
            permission = Permission.objects.get(pk=permission_id)
            remove_perm(permission.codename, user, model_instance)

        return get_user_perms(user, model_instance)

    @classmethod
    def setup_groups(cls, user: AbstractUser):
        if user.is_superuser:
            admin_group, _ = Group.objects.get_or_create(name=SystemGroups.GROUP_ADMIN)
            admin_group_permissions = Permission.objects.filter(
                codename__in=[
                    "manage_forest",
                    "manage_customer",
                    "manage_archive",
                    "view_user",
                    "add_user",
                    "change_user",
                ]
            ).all()
            admin_group.permissions.add(*admin_group_permissions)
            admin_group.user_set.add(user)
            admin_group.save()

            # create normal user group
            member_group, _ = Group.objects.get_or_create(
                name=SystemGroups.GROUP_NORMAL_USER
            )
            member_group_permissions = Permission.objects.filter(
                codename__in=["manage_forest", "manage_customer", "manage_archive"]
            ).all()
            member_group.permissions.add(*member_group_permissions)
            member_group.save()

            # create limited user group
            normal_user_group, _ = Group.objects.get_or_create(
                name=SystemGroups.GROUP_LIMITED_USER
            )
            normal_user_group_permissions = Permission.objects.filter(
                codename__in=["view_forest"]
            ).all()
            normal_user_group.permissions.add(*normal_user_group_permissions)
            normal_user_group.save()

        return cls.serialize_groups(Group.objects.all())

    @classmethod
    def add_to_default_group(cls, user: AbstractUser):
        group, _ = Group.objects.get_or_create(name=SystemGroups.GROUP_LIMITED_USER)
        group.user_set.add(user)
        group.save()

    @classmethod
    def check_policies(cls, request, user, policies):
        policies_to_check = dict()
        for policy in policies:
            try:
                policy_method = import_string(
                    f"hyakumori_crm.permissions.policies.{policy}"
                )
                policies_to_check[policy] = policy_method(request, user)
            except ImportError:
                policies_to_check[policy] = False
                continue

        check_results = all(result is True for _, result in policies_to_check.items())

        return check_results

    @classmethod
    def get_groups(cls):
        return cls.serialize_groups(Group.objects.all())
