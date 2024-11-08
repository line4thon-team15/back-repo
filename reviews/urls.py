from django.urls import path
from .views import ReviewsAPIView, ReviewAPIView, ReviewLikeAPIView

urlpatterns = [
    path('reviews/', ReviewsAPIView.as_view()),
    path('reviews/<int:pk>/', ReviewAPIView.as_view()),
    path('reviews/<int:pk>/like/', ReviewLikeAPIView.as_view()),
]