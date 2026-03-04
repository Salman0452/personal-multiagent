import requests
from langchain.tools import tool

@tool
def get_weather(city: str)->str:
    """
    Get real-time weather for any city in the world.
    Input should be just the city name like 'Berlin' or 'Paris'.
    Returns temperature, weather condition, humidity and wind speed.
    """
    try:
        # Step 1: city name → coordinates (Open-Meteo geocoding)
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_response = requests.get(geo_url, params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        })
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"City '{city}' not found. Try a different spelling."
        
        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        country = location.get("country", "")

        # Step 2: coordinates → weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_response = requests.get(weather_url, params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "timezone": "auto"
        })
        weather_data = weather_response.json()
        current = weather_data["current"]

        # Weather code → human readable
        weather_codes = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy",
            3: "Overcast", 45: "Foggy", 48: "Icy fog",
            51: "Light drizzle", 61: "Slight rain", 63: "Moderate rain",
            65: "Heavy rain", 71: "Slight snow", 73: "Moderate snow",
            75: "Heavy snow", 80: "Slight showers", 81: "Moderate showers",
            95: "Thunderstorm", 99: "Thunderstorm with hail"
        }

        code = current.get("weather_code", 0)
        condition = weather_codes.get(code, f"Code {code}")

        return (
            f"Weather in {city}, {country}:\n"
            f"🌡️  Temperature: {current['temperature_2m']}°C\n"
            f"🌤️  Condition: {condition}\n"
            f"💧  Humidity: {current['relative_humidity_2m']}%\n"
            f"💨  Wind Speed: {current['wind_speed_10m']} km/h"
        )
    except Exception as e:
        return f"Error fetching weather: {str(e)}"