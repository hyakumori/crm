from django.urls import path
from ..archive.rest_api import *

api_urls = [

    path(
        "<str:model>/<uuid:model_pk>/archive/create/", ArchiveCreateApi.as_view(), name="archive_create"
    ),
    path(
        "archives/<uuid:pk>/", ArchiveDetailApi.as_view(), name="archive_detail"
    ),
    path(
        "archives/<uuid:pk>/upload/", ArchiveFileUploadApi.as_view(), name="archive_upload_doc"
    ),
    path(
        "archives/<uuid:pk>/customer/", ArchiveCustomerActionApi.as_view(), name="archive_customer_action"
    ),
    path(
        "archives/<uuid:pk>/customer/<uuid:customer_id>/contacts/<int:add_flag>", ArchiveCustomerContactActionApi.as_view(), name="archive_customer_contact"
    )

]
