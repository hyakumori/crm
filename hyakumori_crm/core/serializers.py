from rest_framework.serializers import ModelSerializer


class AbstractBaseSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'internal_id', 'attributes', 'created_at', 'updated_at')
        abstract = True
