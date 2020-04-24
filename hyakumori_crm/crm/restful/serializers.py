from rest_framework.serializers import (
    ModelSerializer,
    UUIDField,
    IntegerField,
    JSONField,
    SerializerMethodField
)

from ..models import Customer, Contact, Forest, Attachment, Archive


class ContactSerializer(ModelSerializer):
    forest_id = UUIDField(read_only=True)
    cc_attrs = JSONField(read_only=True)

    class Meta:
        model = Contact
        exclude = ["contact_info", "deleted"]


class CustomerSerializer(ModelSerializer):
    self_contact = ContactSerializer()
    forests_count = IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "internal_id",
            "attributes",
            "tags",
            "banking",
            "self_contact",
            "forests_count",
        ]


class ForestSerializer(ModelSerializer):
    class Meta:
        model = Forest
        exclude = ["deleted"]


class AttachmentSerialize(ModelSerializer):
    attachment_file = SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            "id",
            "object_id",
            "content_type",
            "creator",
            "attachment_file",
        ]

    def get_attachment_file(self, obj):
        return obj.attachment_file.name


class ArchiveSerializer(ModelSerializer):
    attachments = list(AttachmentSerialize())

    class Meta:
        model = Archive
        fields = [
            "id",
            "title",
            "content",
            "location",
            "future_response",
            "archive_date",
            "attachments"
        ]
