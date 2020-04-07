from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, constr, validator

from ..core.models import HyakumoriDanticModel, HyakumoriDanticUpdateModel
from ..crm.common import regexes
from ..crm.common.constants import DEFAULT_EMAIL, EMPTY, UNKNOWN


class Name(HyakumoriDanticModel):
    """
    土地所有者名
    漢字	カナ
    kanji   kana
    """

    kanji: str
    kana: str


class Address(HyakumoriDanticModel):
    """
    土地所有者住所
    都道府県	市町村	大字/字
    """

    prefecture: Optional[str]
    municipality: Optional[str]
    sector: Optional[str]


class Contact(BaseModel):
    """
    連絡先情報
    郵便番号	電話番号	携帯電話	メールアドレス
    """

    postal_code: Optional[
        constr(regex=regexes.POSTAL_CODE, strip_whitespace=True)
    ] = "000-0000"
    telephone: Optional[
        constr(regex=regexes.TELEPHONE_NUMBER, strip_whitespace=True)
    ] = "00-0000-0000"
    mobilephone: Optional[
        constr(regex=regexes.MOBILEPHONE_NUMBER, strip_whitespace=True)
    ] = None
    email: EmailStr = DEFAULT_EMAIL


class Banking(BaseModel):
    """
    口座情報
    銀行名	支店名	種類	口座番号	口座名義
    """

    bank_name: Optional[str] = UNKNOWN
    branch_name: Optional[str] = UNKNOWN
    account_type: Optional[str] = EMPTY
    account_number: Optional[constr(regex=regexes.BANKING_ACCOUNT_NUMBER)] = None
    account_name: Optional[str] = UNKNOWN


class CustomerStatus(str, Enum):
    registered = "登録済"
    unregistered = "未登録"


class CustomerInputSchema(BaseModel):
    internal_id: Optional[str]
    name: Name
    address: Address
    contacts: List[Contact] = []
    banking: Banking
    status: CustomerStatus = CustomerStatus.unregistered


class CustomerCreate:
    pass


class CustomerRead:
    pass


class CustomerUpdate:
    pass
