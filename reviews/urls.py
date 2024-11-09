from django.urls import path
from .views import ReviewLikeAPIView, ReviewsAPIView

urlpatterns = [
    path('<int:pk>/delete/', ReviewsAPIView.as_view()),
    path('<int:pk>/update/', ReviewsAPIView.as_view()),
    path('<int:pk>/like/', ReviewLikeAPIView.as_view()),
]