from django.urls import path
from .views import SignUpView, LoginView, LogoutView, CustomTokenRefreshView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('api/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]