import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


@api_view(["POST"])
@permission_classes([])
def oauth(request):
    oauth_resp = requests.post(
        "https://slack.com/api/oauth.v2.access",
        data={
            "client_id": settings.SLACK_CLIENT_ID,
            "client_secret": settings.SLACK_CLIENT_SECRET,
            "code": request.data.get("code"),
        },
    )
    resp_data = oauth_resp.json()
    if resp_data["ok"] is False:
        return Response(resp_data, status=400)
    return Response(resp_data, status=oauth_resp.status_code)
