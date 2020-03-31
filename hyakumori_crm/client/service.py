from django.core.exceptions import ValidationError
from .models import Client


def get(pk):
    try:
        return Client.objects.get(pk=pk)
    except (Client.DoesNotExist, ValidationError):
        raise Client.DoesNotExist


def create(data):
    c = Client(**data)
    c.save()
    return c


def update(client, data):
    return client
