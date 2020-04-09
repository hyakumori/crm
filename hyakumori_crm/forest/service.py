from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connections
from django.db.utils import OperationalError

from ..crm.models.forest import Forest


def get_forests_by_condition(condition):
    if condition:
        page = condition.get('page')
        items_per_page = condition.get('items_per_page')
        order_by = condition.get('order_by')
        is_desc = condition.get('desc')
        items_from = (page - 1) * items_per_page
        items_to = page * items_per_page
        if order_by:
            if is_desc:
                forests = Forest.objects.all().order_by(order_by)[items_from:items_to]
            else:
                forests = Forest.objects.all().order_by(f"-{order_by}")[items_from:items_to]
        else:
            forests = Forest.objects.all().order_by("-internal_id")[items_from:items_to]
        total = Forest.objects.count()
        if forests:
            return {"ok": True, "forests": forests, "total": total}
        else:
            return {"ok": False, "forest": None, "total": 0}
    else:
        return {"ok": False, "forest": None, "total": 0}


# def get(pk):
#     try:
#         return Forest.objects.get(pk=pk)
#     except (Forest.DoesNotExist, ValidationError):
#         return None


# def create(data):
#     forest = Forest(**data)
#     forest.save()
#     return forest
