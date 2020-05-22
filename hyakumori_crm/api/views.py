from django.http import Http404
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view()
def notfound_view(request):
    raise Http404()


@api_view(["GET"])
def maintenance_status(request):
    task_id = cache.get("maintain_task_id")
    return Response({"in_maintain": bool(task_id)})
