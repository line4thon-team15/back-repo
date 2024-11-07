from django.urls import path, include
from rest_framework import routers

from .views import ServiceViewSet

app_name = "services"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("4line-services", ServiceViewSet, basename="4line-services")

urlpatterns = [
    path("", include(default_router.urls)),
] 