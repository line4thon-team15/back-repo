from django.urls import path
from .views import *

urlpatterns = [
    path('route-map/', MainRouteView.as_view(), name='route_map'),
    path('HOF-score/', MainScoreView.as_view(), name='HOF_score'),
    path('HOF-badge/', MainTagView.as_view(), name='HOF_badge'),
    path('recent/', MainRecentView.as_view(), name='recent'),
]