import http.client
import json
import os
from dotenv import load_dotenv
load_dotenv()


def get_weather_and_aqi_data(lat, lng):
    # Create HTTPS connection for the weather API
    weather_conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

    # Define headers for the weather API request
    weather_headers = {
        "x-rapidapi-key": os.getenv("WEATHER_API_KEY"),
        "x-rapidapi-host": os.getenv("WEATHER_API_HOST"),
    }

    # Request current weather data
    weather_conn.request(
        "GET", f"/current.json?q={lat}%2C{lng}", headers=weather_headers
    )
    weather_res = weather_conn.getresponse()
    weather_data = weather_res.read()
    weather_json = json.loads(weather_data.decode("utf-8"))

    # Create HTTPS connection for the AQI API
    aqi_conn = http.client.HTTPSConnection("air-quality-by-api-ninjas.p.rapidapi.com")

    # Define headers for the AQI API request
    aqi_headers = {
        "x-rapidapi-key": "37d82f432bmsh9da3a1d7aee29bdp1f6f0cjsnfb862a21b9be",
        "x-rapidapi-host": "air-quality-by-api-ninjas.p.rapidapi.com",
    }

    # Request air quality data
    aqi_conn.request("GET", f"/v1/airquality?lat={lat}&lon={lng}", headers=aqi_headers)
    aqi_res = aqi_conn.getresponse()
    aqi_data = aqi_res.read()
    aqi_json = json.loads(aqi_data.decode("utf-8"))

    # Combine weather and AQI data into one response
    combined_data = {"weather": weather_json, "aqi": aqi_json}

    return combined_data


# # Example usage:
# lat = 47.6062  # Latitude for Seattle
# lng = -122.3321  # Longitude for Seattle
# data = get_weather_and_aqi_data(lat, lng)
# print(json.dumps(data, indent=2))
