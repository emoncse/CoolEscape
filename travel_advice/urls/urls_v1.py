from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.views_v1 import TravelRecommendationViewSet


urlpatterns = [
    path('travel-destination/', TravelRecommendationViewSet.as_view({'get': 'travel_recommendation'}), ),
]
