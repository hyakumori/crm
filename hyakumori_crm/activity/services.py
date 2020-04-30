from django.contrib.contenttypes.models import ContentType
from django.db import connection

from hyakumori_crm.activity.constants import *
from hyakumori_crm.activity.models import ActionLog
from hyakumori_crm.core.utils import get_remote_ip
from hyakumori_crm.crm.models.message_template import MessageTemplate


class ActivityService:

    @classmethod
    def import_message_templates(cls, for_type: str, action_class):
        records = []
        actions = dict([(k, v) for (k, v) in action_class.__dict__.items() if isinstance(v, tuple)])
        for name, message in actions.items():
            content_type = ContentType.objects.get_for_model(ActionLog)
            name = message[0]
            template = message[1]
            icon = message[2]
            message_template = MessageTemplate(
                name=name, template=template, language="ja_JP",
                content_type=content_type
            )
            message_template.attributes["icon"] = icon
            message_template.attributes["content_type"] = for_type
            records.append(message_template)

        return MessageTemplate.objects.bulk_create(records, ignore_conflicts=True)

    @classmethod
    def log(cls, action, model_instance, user=None,
            remote_ip=None, template_data=None, changes=None,
            request=None):
        """
        Usage:
        >>> from hyakumori_crm.crm.models import Forest
        >>> forest = Forest.objects.first()
        >>> ActivityService.log(ForestActions.created, forest)
        """

        if changes is None:
            changes = {}

        if request is not None:
            if remote_ip is None:
                remote_ip = get_remote_ip(request)
            if user is None and request.user is not None:
                user = request.user

        try:
            template_name = action[0] if isinstance(action, tuple) else action
            template = MessageTemplate.objects.get(name=template_name)
            content_type = ContentType.objects.get_for_model(model_instance)

            return ActionLog.objects.create(
                content_type=content_type,
                object_pk=model_instance.pk,
                template_name=template.name,
                template_data=template_data,
                changes=changes,
                user=user,
                remote_ip=remote_ip
            )
        except MessageTemplate.DoesNotExist:
            return ActionLog.objects.none()

    @classmethod
    def get_log_for_object(cls, lang_code, app_label, object_type, object_id):
        content_type = ContentType.objects.filter(app_label=app_label, model=object_type).first()
        action_content_type = ContentType.objects.get_for_model(ActionLog)

        with connection.cursor() as cursor:
            query = """
                select
                    al.object_pk,
                    al.user_id, al.changes, al.created_at, al.remote_ip, al.template_data,
                    cm.attributes, cm.template, uu.first_name, uu.last_name,
                    uu.email, uu.username
                from activity_actionlog al
                join crm_messagetemplate cm on al.template_name = cm.name and cm.language=%s
                join users_user uu on al.user_id = uu.id
                where al.object_pk::uuid=%s::uuid and al.content_type_id=%s and cm.content_type_id=%s
                order by al.created_at
            """
            cursor.execute(query, [lang_code, object_id, content_type.pk, action_content_type.pk])
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        return results
