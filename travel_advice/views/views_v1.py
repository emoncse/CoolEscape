import asyncio
import logging
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from common_services.districts_names import district_names_for_swagger as district_names
from common_services.weather_helper import WeatherService
from common_services.districts_names import processed_json_data

districts = processed_json_data()

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@extend_schema(tags=['Travel Advice'])
class TravelRecommendationViewSet(ViewSet):
    """API ViewSet for travel recommendation based on weather."""

    @extend_schema(
        summary="Travel Weather Recommendation",
        description="Compare the 2 PM temperatures of the friend's location and destination for the given travel date. "
                    "Recommends if traveling is ideal based on temperature difference.",
        parameters=[
            OpenApiParameter(
                name="friend_district",
                description="District name of friend's location (from bd-districts.json)",
                required=True,
                type=OpenApiTypes.STR,
                enum=district_names()
            ),
            OpenApiParameter(
                name="destination_district",
                description="District name of destination (from bd-districts.json)",
                required=True,
                type=OpenApiTypes.STR,
                enum=district_names()
            ),
            OpenApiParameter(
                name="date",
                description="Travel date in YYYY-MM-DD format",
                required=True,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            200: {
                "description": "Returns the temperatures of both locations at 2 PM and travel recommendation.",
                "content": {
                    "application/json": {
                        "example": {
                            "friend_temperature": 27.5,
                            "destination_temperature": 26.8,
                            "decision": "Yes, it's a good day to travel!"
                        }
                    }
                }
            },
            400: {
                "description": "Bad request due to missing parameters.",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "All parameters (friend_district, destination_district, date) are required"
                        }
                    }
                }
            }
        }
    )
    def travel_recommendation(self, request):
        """Compare friend's location and destination weather at 2 PM on a given travel date."""

        friend_district_name = request.query_params.get("friend_district")
        destination_district_name = request.query_params.get("destination_district")
        travel_date = request.query_params.get("date")

        logger.info("Received request: friend_district=%s, destination_district=%s, date=%s",
                    friend_district_name, destination_district_name, travel_date)

        if friend_district_name and destination_district_name:
            friend_district_data = next(
                (district for district in districts if district["name"] == friend_district_name), None)
            destination_district_data = next(
                (district for district in districts if district["name"] == destination_district_name), None)

            if not friend_district_data or not destination_district_data:
                logger.error("Invalid district name(s) provided.")
                return Response({"error": "Invalid district name(s) provided."}, status=400)

            friend_latitude, friend_longitude = float(friend_district_data["lat"]), float(friend_district_data["long"])
            destination_latitude, destination_longitude = float(destination_district_data["lat"]), float(
                destination_district_data["long"])
        else:
            friend_latitude = request.query_params.get("friend_lat")
            friend_longitude = request.query_params.get("friend_lon")
            destination_latitude = request.query_params.get("dest_lat")
            destination_longitude = request.query_params.get("dest_lon")

            if not all([friend_latitude, friend_longitude, destination_latitude, destination_longitude]):
                logger.error("Either district names or latitude/longitude values are required.")
                return Response({"error": "Either district names or latitude/longitude values are required."},
                                status=400)

            friend_latitude, friend_longitude = float(friend_latitude), float(friend_longitude)
            destination_latitude, destination_longitude = float(destination_latitude), float(destination_longitude)

        if not travel_date:
            logger.error("Travel date is required.")
            return Response({"error": "Travel date is required."}, status=400)

        logger.info("Fetching weather data for coordinates: friend=(%s, %s), destination=(%s, %s) on %s",
                    friend_latitude, friend_longitude, destination_latitude, destination_longitude, travel_date)

        weather_data = asyncio.run(WeatherService.compare_travel_weather(
            float(friend_latitude), float(friend_longitude), float(destination_latitude), float(destination_longitude), travel_date
        ))

        logger.info("Weather data response: %s", weather_data)
        return Response(weather_data)
