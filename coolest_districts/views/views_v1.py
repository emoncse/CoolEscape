from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from common_services.weather_helper import WeatherService
import logging

logger = logging.getLogger(__name__)


@extend_schema(tags=['Coolest Districts'])
class DistrictWeatherViewSet(viewsets.ViewSet):
    """API ViewSet for fetching district-wise average temperatures at 2 PM."""
    # permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get Coolest Districts",
        description="Fetches the districts with the lowest average temperatures at 2 PM, with optional sorting and pagination.",
        parameters=[
            OpenApiParameter(
                name="limit",
                description="Number of districts to return",
                required=False,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name="sort",
                description="Sort order (asc/desc)",
                required=False,
                type=OpenApiTypes.STR,
                enum=["asc", "desc"]
            ),
        ],
        responses={
            200: {
                "description": "List of coolest districts sorted by temperature.",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": "40",
                                "division_id": "2",
                                "name": "Bandarban",
                                "bn_name": "বান্দরবান",
                                "average_temperature": 30.27,
                                "temperature_unit": "Celsius",
                                "latitude": "22.1953275",
                                "longitude": "92.2183773"
                            },
                            {
                                "id": "39",
                                "division_id": "1",
                                "name": "Pirojpur",
                                "bn_name": "পিরোজপুর",
                                "average_temperature": 29.83,
                                "temperature_unit": "Celsius",
                                "latitude": "22.5841",
                                "longitude": "89.9720"
                            }
                        ]
                    }
                }
            },
            400: {
                "description": "Invalid parameters provided.",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "Invalid sort parameter. Use 'asc' or 'desc'."
                        }
                    }
                }
            }
        }
    )
    def get_coolest_districts(self, request):
        """Returns sorted district-wise weather data."""
        weather_data = WeatherService.fetch_weather_data_sync()

        limit = int(request.query_params.get("limit", 10))
        sort_order = request.query_params.get("sort", "asc").lower()

        if sort_order == "desc":
            weather_data = sorted(weather_data, key=lambda x: x.get("average_temperature", float("inf")), reverse=True)

        logger.info(f"Returning {len(weather_data)} coolest districts.")
        return Response(weather_data[:limit])
