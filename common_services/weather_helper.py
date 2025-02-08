import asyncio
import aiohttp
import json
import re
from utils.base_urls import get_forecast_url
from common_services.districts_names import processed_json_data
import logging
from django.core.cache import cache
from common_services.hash_key_generate import sanitize_cache_key

CACHE_EXPIRATION = 600

logger = logging.getLogger(__name__)

time_pattern = re.compile(r"T14:00$")
district_list = processed_json_data()


class WeatherService:
    """Service to fetch district-wise weather data asynchronously."""

    @staticmethod
    async def fetch_weather_data(session, district_info):
        """Fetch weather data for a single district."""
        request_params = {
            "latitude": float(district_info["lat"]),
            "longitude": float(district_info["long"]),
            "hourly": "temperature_2m",
            "timezone": "Asia/Dhaka"
        }

        try:
            logger.info(f"Fetching weather data for {district_info['name']} with params: {request_params}")
            async with session.get(get_forecast_url(), params=request_params) as api_response:
                if api_response.status != 200:
                    logger.error(f"API Error {api_response.status} for district: {district_info['name']}")
                    return {
                        "district": district_info["name"],
                        "error": f"API Error {api_response.status}"
                    }

                weather_data = await api_response.json()
                logger.debug(f"Response received for {district_info['name']}: {weather_data}")

                if "hourly" not in weather_data or "time" not in weather_data["hourly"] or "temperature_2m" not in weather_data["hourly"]:
                    logger.warning(f"No hourly data available for {district_info['name']}")
                    return {
                        "district": district_info["name"],
                        "error": "No hourly data available"
                    }

                time_entries = weather_data['hourly']['time']
                temperature_entries = weather_data['hourly']['temperature_2m']

                matching_indices = [i for i, time_entry in enumerate(time_entries) if time_pattern.search(time_entry)]

                if not matching_indices:
                    logger.warning(f"No matching time slots found for {district_info['name']}")
                    return {
                        "district": district_info["name"],
                        "message": "No temperature data available for the requested time"
                    }

                average_temperature = sum(temperature_entries[i] for i in matching_indices) / len(matching_indices) if matching_indices else None
                logger.info(f"Average temperature for {district_info['name']}: {average_temperature}")
                result = {
                    "id": district_info["id"],
                    "division_id": district_info["division_id"],
                    "name": district_info["name"],
                    "bn_name": district_info["bn_name"],
                    "average_temperature": round(average_temperature, 2),
                    "temperature_unit": "Celsius",
                    "latitude": district_info["lat"],
                    "longitude": district_info["long"]
                }
                # Store result in Django cache
                cache_key = sanitize_cache_key(district_info['name'])
                cache.set(cache_key, result, CACHE_EXPIRATION)
                return result

        except Exception as error:
            logger.exception(f"Error fetching weather data for {district_info['name']}: {error}")
            return {
                "district": district_info["name"],
                "error": str(error),
                "message": "An error occurred while fetching data"
            }

    @classmethod
    async def retrieve_district_weather_data(cls):
        weather_results = []
        async with aiohttp.ClientSession() as http_session:
            async_tasks = []
            for district in district_list:
                cache_key = sanitize_cache_key(district['name'])
                cached_entry = cache.get(cache_key)
                if cached_entry:
                    logger.info(f"Using cached data for {district['name']}")
                    weather_results.append(cached_entry)
                else:
                    async_tasks.append(cls.fetch_weather_data(http_session, district))

            if async_tasks:
                weather_responses = await asyncio.gather(*async_tasks)
                weather_results.extend(weather_responses)

        logger.info("Weather data fetching complete.")
        return sorted(weather_results, key=lambda x: x.get("average_temperature", float("inf")))

    @classmethod
    def fetch_weather_data_sync(cls):
        logger.info("Starting synchronous weather fetching...")
        return asyncio.run(cls.retrieve_district_weather_data())