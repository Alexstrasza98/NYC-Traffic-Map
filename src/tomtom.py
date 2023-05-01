import time

import requests
import json
import os
from typing import Dict, List, Tuple
from tqdm import tqdm
import aiohttp
import asyncio

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
TRAFFIC_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={}&zoom={}&key={}"
INCIDENT_URL = "https://api.tomtom.com/traffic/services/5/incidentDetails?key={}&bbox={}&language=en-GB&t=1111&timeValidityFilter=present"

global count
count = 0


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
        url = TRAFFIC_URL.format(coordinate, zoom, API_KEY)
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
    url = INCIDENT_URL.format(API_KEY, bbox)
    response = requests.get(url)
    data = json.loads(response.text)["incidents"]

    for incident in data:
        # Extract incident data
        incident_data = {
            "geometry_type": incident["geometry"]["type"],
            "coordinates": incident["geometry"]["coordinates"],
            "incident_type": incident["properties"]["iconCategory"],
        }

        all_data.append(incident_data)

    return all_data


async def get_traffic_data_async(coord_rdd, zoom, API_KEY):
    # for line in coord_rdd.map(lambda row: row[0]).collect():
    #     print(line)
    async with aiohttp.ClientSession() as session:
        responses = []
        for line in coord_rdd.map(lambda row: row[0]).collect():
            single_response = asyncio.ensure_future(single_call(session, line, zoom, API_KEY))
            responses.append(single_response)
        tomtom = await asyncio.gather(*responses)
    print(tomtom)
    return tomtom

async def single_call(session, coord, zoom, API_KEY):
    url_traffic = TRAFFIC_URL.format(coord, zoom, API_KEY)
    # print(url_traffic)
    async with session.get(url_traffic) as response:
        content_type = response.headers.get('content-type')
        if content_type != "application/json":
            result_data = await response.json()
        else:
            # if detects xml:
            #   scenario 1: ran out of all the requests, then probably should just finish everything. (here will it be reseted for another 15 minus?)
            #   scenatio 2: ran out of the request for 1 second, wait 1 second.
            #seem like the best solution is to downsample (condsidering the demo and limited requests)

            time.sleep(1)
        print(content_type)
        print(type(content_type))
        try:
            return result_data
        except:
            return None


