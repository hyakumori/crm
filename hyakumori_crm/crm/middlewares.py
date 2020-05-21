import os.path
from django.http import HttpResponse, JsonResponse
from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = "Service temporarily unavailable, try again later."
    default_code = "service_unavailable"


def in_maintain_middleware(get_response):
    def middleware(request):
        if os.path.exists("in_maintain.lck"):
            print(request.path)
            if request.path.startswith("/api/v1") or request.path.startswith(
                "/graphql"
            ):
                return JsonResponse({"detail": "Service Unavailable"}, status=503)
            else:
                return HttpResponse("Service Unavailable", "text/plain", 503)
        resp = get_response(request)

        return resp

    return middleware
