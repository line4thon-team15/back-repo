from django.urls import include, path
from .views import SignUpView, LoginView, LogoutView, CustomTokenRefreshView, ProfileView

# mypage_router = routers.SimpleRouter(trailing_slash=False)
# mypage_router.register("mypage", MyPageViewSet, basename="mypage")

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('api/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('mypage', ProfileView.as_view(), name="mypage")
]