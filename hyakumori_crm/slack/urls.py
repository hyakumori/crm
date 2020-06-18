from django.urls import path

from .restful import oauth, test, list_installs


api_urls = [
    path("slack/oauth", oauth),
    path("slack/test", test),
    path("slack/installs", list_installs),
]
