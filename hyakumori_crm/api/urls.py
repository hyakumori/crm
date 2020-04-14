from rest_framework.routers import DefaultRouter
from hyakumori_crm.forest.urls import api_urls as forest_api_urls

from hyakumori_crm.customer.urls import api_urls as customer_api_urls
from hyakumori_crm.users.urls import api_urls as user_api_urls

router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns += forest_api_urls + customer_api_urls + user_api_urls
