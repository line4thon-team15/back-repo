from django.urls import path, include
from rest_framework import routers

from .views import *
from reviews.views import ReviewsAPIView

app_name = "services"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("4line-services", ServiceViewSet, basename="4line-services")

member_router = routers.SimpleRouter(trailing_slash=False)
member_router.register("member", MemberViewSet, basename="member")

presentation_router = routers.SimpleRouter(trailing_slash=False)
presentation_router.register("presentation", PresentationViewSet, basename="presenstation")

my_service_router = routers.SimpleRouter(trailing_slash=False)
my_service_router.register("my-service", MyServiceViewset, basename="my-service")

urlpatterns = [
    path("", include(default_router.urls)),
    path("", include(member_router.urls)),
    path("", include(presentation_router.urls)),
    path("", ServiceListView.as_view(), name='service-list'),
    path("4line-services/<int:service_id>/", ReviewsAPIView.as_view()),
    path("4line-services/<int:service_id>/reviews/<int:review_id>/", ReviewsAPIView.as_view()),
    path("upload-team-data/", TeamDataView.as_view(), name="upload_team_data"),
    path("", include(my_service_router.urls))
] 