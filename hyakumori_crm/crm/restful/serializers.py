from rest_framework.serializers import ModelSerializer, UUIDField, IntegerField, SlugRelatedField

from ..models import  Customer, Contact, Forest, Archive, Attachment, ArchiveCustomer, ArchiveForest
from hyakumori_crm.core.serializers import AbstractBaseSerializer

class ContactSerializer(ModelSerializer):
    forest_id = UUIDField(read_only=True)

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


class ArchiveCustomerSerializer(ModelSerializer):

    class Meta:
        model = ArchiveCustomer
        fields = ('archive', 'customer', )

    customer = CustomerSerializer()


class ArchiveForestSerializer(ModelSerializer):

    class Meta:
        model = ArchiveForest
        fields = ('archive', 'forest')

    forest = ForestSerializer()


class AttachmentSerializer(AbstractBaseSerializer):
    class Meta:
        model = Attachment
        fields = ('content_type', 'object_id', 'attachment_file', 'creator')
    creator = SlugRelatedField(read_only=True,
        slug_field='id'
    )


class ArchiveSerializer(AbstractBaseSerializer):
    class Meta:
        model = Archive
        fields = AbstractBaseSerializer.Meta.fields + ('consult_date', 'location', 'future_action', 'discuss_content', 'attachment_list', 'archivecustomer_set', 'archiveforest_set', 'creator')

    attachment_list = AttachmentSerializer(many=True)
    archivecustomer_set = ArchiveCustomerSerializer(many=True)
    archiveforest_set =  ArchiveForestSerializer(many=True)
    creator = SlugRelatedField(read_only=True,
                               slug_field='id'
                               )
