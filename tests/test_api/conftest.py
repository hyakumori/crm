import pytest
from rest_framework.test import APIRequestFactory
from hyakumori_crm.users.models import User
from hyakumori_crm.crm.models import Forest
from hyakumori_crm.crm.schemas.contract import ContractType


@pytest.fixture()
def api_rf():
    return APIRequestFactory()


@pytest.fixture()
def admin_user():
    return User.objects.create_superuser(
        email="admin@example.com", password="testp4sswrd"
    )


@pytest.fixture
def forest():
    return Forest.objects.create(
        cadastral={"prefecture": "foo", "municipality": "foo", "sector": "foo"},
        contracts=[{"type": ContractType.long_term}],
    )
