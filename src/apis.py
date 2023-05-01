import json
import os
from typing import Dict, List, Tuple

import requests
from dotenv import load_dotenv
from tqdm import tqdm

from utils import get_centerpoint

load_dotenv()

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
TRAFFIC_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={}&zoom={}&key={}"
INCIDENT_URL = "https://api.tomtom.com/traffic/services/5/incidentDetails?key={}&bbox={}&language=en-GB&t=1111&timeValidityFilter=present"
WEARTHER_URL = "https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={}&lon={}&appid={}"

def get_traffic_data(coordinates: List[Tuple], zoom: int) -> List[Dict]:
    """
    Get speed information from TomTom API.

    Params:
        coordinates: List of coordinates (lat, lon) to get speed information for
        zoom: Zoom level of the map

    Returns:
        speed_data: a json object containing speed information for each coordinate
    """
    expected_columns = [
        "currentSpeed",
        "freeFlowSpeed",
        "currentTravelTime",
        "freeFlowTravelTime",
        "roadClosure",
        "coordinates",
        "frc",
    ]

    all_data = []

    for coordinate in tqdm(coordinates):
        # Send request and parse response
        url = TRAFFIC_URL.format(coordinate, zoom, TOMTOM_API_KEY)
        response = requests.get(url)
        data = json.loads(response.text)["flowSegmentData"]

        # Extract traffic data
        traffic_data = {
            key: value for key, value in data.items() if key in expected_columns
        }

        traffic_data["coordinates"] = traffic_data["coordinates"]["coordinate"]

        all_data.append(traffic_data)

    return all_data


def get_incident_data(bbox: str) -> List[Dict]:
    """
    Get incident information from TomTom API.

    Params:
        bbox: Bounding box of the map to get incident information for

    Returns:
        incident_data: a json object containing incident information inside bounding box
    """

    all_data = []

    # Send request and parse response
    url = INCIDENT_URL.format(TOMTOM_API_KEY, bbox)
    response = requests.get(url)
    data = json.loads(response.text).get("incidents", [])

    for incident in data:
        # Extract incident data
        incident_data = {
            "geometry_type": incident["geometry"]["type"],
            "coordinate": get_centerpoint(incident["geometry"]["coordinates"]),
            "incident_type": incident["properties"]["iconCategory"],
        }

        all_data.append(incident_data)

    return all_data


def get_weather_data(coordinates: List[Tuple]) -> List[Dict]:

    all_data = []

    for coordinate in tqdm(coordinates):
        lat, lon = coordinate.split(",")
        url = WEARTHER_URL.format(lat, lon, WEATHER_API_KEY)
        data = requests.get(url).json()

        current_data = data['list'][0]

        rain = current_data.get('rain', {}).get('1h', 0)
        wind_speed = current_data['wind']['speed']
        temp = current_data['main']['temp']
        humidity = current_data['main']['humidity']
        visibility = current_data.get('visibility', 0)
        weather = current_data['weather'][0]['main']

        weather_data = {
            "coordinate": coordinate,
            "temperature": temp,
            "humidity": humidity,
            "rain": rain,
            "wind_speed": wind_speed,
            "visibility": visibility,
            "weather": weather,
        }

        all_data.append(weather_data)

    return all_data