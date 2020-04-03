from ...core.models import BaseResourceModel, JSONField
from ..schemas.contract import Contract
from ..schemas.forest import Cadastral, ForestOwner, GeoData, Tag


class DefaultForest:
    @staticmethod
    def cadastral():
        return Cadastral().dict()

    @staticmethod
    def owner():
        return ForestOwner().dict()

    @staticmethod
    def contract():
        return Contract().dict()

    @staticmethod
    def tag():
        return Tag().dict()

    @staticmethod
    def geodata():
        return GeoData().dict()


class Forest(BaseResourceModel):
    cadastral = JSONField(default=DefaultForest.cadastral, blank=True, null=True)
    owner = JSONField(default=DefaultForest.owner, blank=True, null=True)
    contract = JSONField(default=DefaultForest.contract, blank=True, null=True)
    tag = JSONField(default=DefaultForest.tag, blank=True, null=True)
    geodata = JSONField(default=DefaultForest.geodata, blank=True, null=True)
