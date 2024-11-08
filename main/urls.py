from django.urls import path
from .views import *

urlpatterns = [
    path('route-map/', MainRouteView.as_view(), name='route_map'),
    path('HOF-score/', MainScoreView.as_view(), name='main_HOF_score'),
    path('random/', MainRandomView.as_view(), name='random'),
]