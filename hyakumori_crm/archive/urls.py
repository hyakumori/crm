from django.urls import path

from .restful import *

api_urls = [
    path("archives", archives),
    path("archives/<uuid:pk>", archive),
    path("archives/<uuid:pk>/forests", archive_forests),
    path("archives/<uuid:pk>/customers", archive_customers),
    path("archives/<uuid:archive_pk>/attachments", attachments),
    path("archives/<uuid:archive_pk>/attachments/<uuid:attachment_pk>", attachment)
]
