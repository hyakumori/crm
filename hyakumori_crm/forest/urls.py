from rest_framework import viewsets, routers
from django.urls import path
from .restful import ForestViewSets, update

router = routers.SimpleRouter(trailing_slash=False)
router.register("forests", ForestViewSets, basename="forest")

api_urls = router.urls + [path("forests/<uuid:pk>", view=update, name="forests-update")]
