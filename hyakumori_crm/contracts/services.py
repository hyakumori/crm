from .models import ContractType
from hyakumori_crm.crm.schemas.contract import ContractType as ContractTypeEnum


class ContractService:
    @classmethod
    def setup_contracts(cls):
        for contract_type in ContractTypeEnum:
            contract_type_instance, _ = ContractType.objects.get_or_create(name=contract_type.value)
            contract_type_instance.attributes["assignable"] = contract_type.name != "fsc"
            contract_type_instance.code = contract_type.name
            contract_type_instance.description = contract_type.value
            contract_type_instance.save()
