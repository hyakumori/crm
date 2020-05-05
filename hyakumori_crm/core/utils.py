from itertools import chain

from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse, HttpResponseBadRequest

from hyakumori_crm.crm.restful.paginations import StandardPagination


def get_remote_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        remote_ip = x_forwarded_for.split(',')[0]
    else:
        remote_ip = request.META.get('REMOTE_ADDR')

    return remote_ip


def model_to_dict(instance, fields=None, exclude=None):
    """
    Copy from django.form.models
    Tweak to remove ``editable`` conditions, by default return all infos
    ----------
    Return a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    return data


def default_paginator():
    paginator = StandardPagination()

    return paginator


def make_error_json(message: str, status=HttpResponseBadRequest.status_code):
    return JsonResponse(
        status=status, data=dict(detail=message)
    )


def make_success_json(data: any):
    return JsonResponse(data=data)
