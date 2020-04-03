from .models import Forest
from django.core.exceptions import ValidationError
import json
import os

def get_all():
    f = load_dummy_data()
    if f is None:
        return {
            "ok": False,
            "forest": None
        }
    else:
        data = f.read()
        forests = json.loads(data)
        return {
            "ok": True,
            "forests": forests if forests else None
        }

def get(pk):
    try:
        return Forest.objects.get(pk=pk)
    except (Forest.DoesNotExist, ValidationError):
        return None

def create(data):
    forest = Forest (**data)
    forest.save()
    return forest

def load_dummy_data():
    dummyDataDir = os.path.join(os.getcwd(), "hyakumori_crm/dummy", "forest_data.json")
    return open(dummyDataDir, 'r')
