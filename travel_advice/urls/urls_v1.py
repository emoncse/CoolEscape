from django.urls import path
from travel_advice.views.views_v1 import TravelRecommendationViewSet

urlpatterns = [
    path('travel-recommendation/', TravelRecommendationViewSet.as_view({'get': 'travel_recommendation'})),
]
