import argparse
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import schedule
import time
import logging
from geopy.geocoders import Nominatim
import folium
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# OpenWeatherMap API endpoint
API_ENDPOINT = "http://api.openweathermap.org/data/2.5/forecast"
def get_coordinates(location):
    """Get latitude and longitude for a given location."""
    geolocator = Nominatim(user_agent="weather_data_vision")
    try:
        location_data = geolocator.geocode(location)
        return location_data.latitude, location_data.longitude
    except:
        logger.error(f"Unable to find coordinates for {location}")
        return None, None
def fetch_weather_data(api_key, location, units='metric'):
    """Fetch weather data from OpenWeatherMap API."""
    lat, lon = get_coordinates(location)
    if lat is None or lon is None:
        return None
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': units
    }
    try:
        response = requests.get(API_ENDPOINT, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return None
def parse_weather_data(data):
    """Parse the raw weather data into a more usable format."""
    if not data or 'list' not in data:
        return None
    parsed_data = []
    for item in data['list']:
        parsed_data.append({
            'datetime': datetime.fromtimestamp(item['dt']),
            'temperature': item['main']['temp'],
            'humidity': item['main']['humidity'],
            'wind_speed': item['wind']['speed'],
            'description': item['weather'][0]['description']
        })
    return parsed_data
def create_temperature_chart(data, location):
    """Create a temperature chart using matplotlib."""
    dates = [item['datetime'] for item in data]
    temps = [item['temperature'] for item in data]
    plt.figure(figsize=(12, 6))
    plt.plot(dates, temps, marker='o')
    plt.title(f"Temperature Forecast for {location}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('temperature_forecast.png')
    plt.close()
def create_weather_map(location, lat, lon):
    """Create a folium map with the location marker."""
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], popup=location).add_to(m)
    m.save("weather_location_map.html")
def display_current_weather(data, location):
    """Display current weather information in the console."""
    current = data[0]
    print(f"\nCurrent Weather for {location}:")
    print(f"Temperature: {current['temperature']}°C")
    print(f"Humidity: {current['humidity']}%")
    print(f"Wind Speed: {current['wind_speed']} m/s")
    print(f"Description: {current['description']}")
def weather_data_vision(api_key, location, update_frequency):
    """Main function to fetch, process, and visualize weather data."""
    logger.info(f"Fetching weather data for {location}")
    data = fetch_weather_data(api_key, location)
    if not data:
        logger.error("Failed to fetch weather data")
        return
    parsed_data = parse_weather_data(data)
    if not parsed_data:
        logger.error("Failed to parse weather data")
        return
    display_current_weather(parsed_data, location)
    create_temperature_chart(parsed_data, location)
    lat, lon = get_coordinates(location)
    if lat and lon:
        create_weather_map(location, lat, lon)
    logger.info("Weather data processing complete")
def schedule_updates(api_key, location, update_frequency):
    """Schedule periodic updates of weather data."""
    schedule.every(update_frequency).hours.do(weather_data_vision, api_key, location, update_frequency)
    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    Weather Data Vision: A script to fetch, process, and visualize weather data.
    How to use:
    1. Obtain an API key from OpenWeatherMap (https://openweathermap.org/api)
    2. Run the script with your API key, desired location, and update frequency
    3. View the generated charts and maps in the script's directory
    Example:
    python weather_data_vision.py --api_key YOUR_API_KEY --location "New York" --update_frequency 3
    """)
    parser.add_argument('--api_key', required=True, help='Your OpenWeatherMap API key')
    parser.add_argument('--location', required=True, help='Location for weather data (e.g., "New York")')
    parser.add_argument('--update_frequency', type=int, default=1, help='Update frequency in hours (default: 1)')
    args = parser.parse_args()
    try:
        # Initial run
        weather_data_vision(args.api_key, args.location, args.update_frequency)
        # Schedule updates
        schedule_updates(args.api_key, args.location, args.update_frequency)
    except KeyboardInterrupt:
        logger.info("Script terminated by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")