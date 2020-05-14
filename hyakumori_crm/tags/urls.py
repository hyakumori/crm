from django.urls import path

from .restful import *


api_urls = [
    path("tags/setup-tags", setup_tags),
    path("tags/settings/<str:app_name>/<str:object_type>", get_settings_for_type),
    path("tags/<str:app_name>/<str:object_type>", get_tags_for_type),
    path("tags/<str:app_name>/<str:object_type>/modify", modify_tag_for_type),
    path("tags/<str:app_name>/<str:object_type>/delete", delete_tag_for_type),
    path("tags/<str:app_name>/<str:object_type>/assign", assign_tag_for_object),
]
