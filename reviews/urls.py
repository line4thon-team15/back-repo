from django.urls import path
from .views import ReviewsAPIView, ReviewAPIView, ReviewLikeAPIView

urlpatterns = [
    path('', ReviewsAPIView.as_view()),
    path('<int:pk>/', ReviewAPIView.as_view()),
    path('<int:pk>/like/', ReviewLikeAPIView.as_view()),
    path('service/<int:service_id>/', ReviewsAPIView.as_view()),
]