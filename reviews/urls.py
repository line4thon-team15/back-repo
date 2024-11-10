from django.urls import path
from .views import ReviewLikeAPIView, ReviewsAPIView

urlpatterns = [
    path('<int:pk>/', ReviewsAPIView.as_view()),
    path('<int:pk>/like/', ReviewLikeAPIView.as_view()),
]