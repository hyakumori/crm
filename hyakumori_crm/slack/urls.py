from django.urls import path

from .restful import oauth


api_urls = [path("slack/oauth", oauth)]
