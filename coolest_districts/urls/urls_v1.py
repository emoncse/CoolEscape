from django.urls import path, include
from ..views.views_v1 import DistrictWeatherViewSet


urlpatterns = [
    path('coolest-districts/', DistrictWeatherViewSet.as_view({'get': 'get_coolest_districts'})),
]