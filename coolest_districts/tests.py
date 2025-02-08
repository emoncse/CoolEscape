from django.test import TestCase
from django.test.client import RequestFactory
from unittest.mock import patch
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from coolest_districts.views.views_v1 import DistrictWeatherViewSet

class DistrictWeatherViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DistrictWeatherViewSet.as_view({"get": "get_coolest_districts"})  # Directly call view method
        self.url = "/v1/coolest-districts/"

    @patch("common_services.weather_helper.WeatherService.fetch_weather_data_sync", return_value=[
        {"id": "31", "division_id": "6", "name": "Panchagarh", "average_temperature": 24.14},
        {"id": "33", "division_id": "6", "name": "Thakurgaon", "average_temperature": 24.27},
        {"id": "26", "division_id": "6", "name": "Dinajpur", "average_temperature": 25.19},
        {"id": "28", "division_id": "6", "name": "Kurigram", "average_temperature": 25.3},
        {"id": "30", "division_id": "6", "name": "Nilphamari", "average_temperature": 25.37},
        {"id": "29", "division_id": "6", "name": "Lalmonirhat", "average_temperature": 25.41},
        {"id": "32", "division_id": "6", "name": "Rangpur", "average_temperature": 25.57},
        {"id": "27", "division_id": "6", "name": "Gaibandha", "average_temperature": 26.03},
        {"id": "5", "division_id": "8", "name": "Jamalpur", "average_temperature": 26.29},
        {"id": "16", "division_id": "8", "name": "Sherpur", "average_temperature": 26.29},
    ])
    def test_get_coolest_districts(self, mock_fetch_weather_data):
        request = self.factory.get(self.url, {"limit": 10, "sort": "asc"})  # Mock GET request
        response = self.view(request)  # Directly call the view

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

        expected_sorted_names = [
            "Panchagarh", "Thakurgaon", "Dinajpur", "Kurigram", "Nilphamari",
            "Lalmonirhat", "Rangpur", "Gaibandha", "Jamalpur", "Sherpur"
        ]

        actual_sorted_names = [district["name"] for district in response.data]
        self.assertEqual(actual_sorted_names, expected_sorted_names, "Sorting order is incorrect!")
