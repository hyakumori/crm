import json

from cryptography.fernet import Fernet
from django.core.serializers.json import DjangoJSONEncoder

key = Fernet.generate_key()
fernet = Fernet(key)


class EncryptError(Exception):
    pass


class DecryptError(Exception):
    pass


def encrypt_string(data, from_dict=True):
    try:
        if from_dict:
            data = json.dumps(data, cls=DjangoJSONEncoder).encode("utf8")
        return fernet.encrypt(data).decode("utf8")
    except:
        raise EncryptError


def decrypt_string(data, to_dict=True):
    try:
        content = fernet.decrypt(data.encode("utf8"))
        if to_dict:
            return json.loads(content)
        return content
    except:
        raise DecryptError


def get_customer_name(name_dict):
    customer_name = ""
    if name_dict.get("last_name", None) is not None:
        customer_name = name_dict.get("last_name")
    if name_dict.get("first_name", None) is not None:
        customer_name += name_dict.get("first_name")

    return customer_name
