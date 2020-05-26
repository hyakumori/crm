from rest_framework.viewsets import ModelViewSet

from .models import ContractType
from .serializers import ContractTypeSerializer
from ..permissions import IsAdminOrReadOnly


class ContractTypeViewSets(ModelViewSet):
    queryset = ContractType.objects.all()
    serializer_class = ContractTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
