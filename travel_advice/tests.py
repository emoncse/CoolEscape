from django.test import TestCase
from unittest.mock import AsyncMock, patch
from common_services.weather_helper import WeatherService


class TravelRecommendationLogicTest(TestCase):
    @patch("common_services.weather_helper.WeatherService.compare_travel_weather", new_callable=AsyncMock)
    async def test_compare_travel_weather(self, mock_compare_weather):
        mock_compare_weather.return_value = {
            "friend_temperature": 27.5,
            "destination_temperature": 26.8,
            "decision": "Yes, it's a good day to travel!"

        }

        result = await WeatherService.compare_travel_weather("Dhaka", "Chattogram","2024-02-10")

        self.assertEqual(result["decision"], "Yes, it's a good day to travel!")
