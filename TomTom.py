import requests
import json
from typing import List, Dict
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv('.env'))
import os
env_dist = os.environ
# print(type(env_dist.get('TomTomAPIKey')))
apikey =env_dist.get('TomTomAPIKey')


def get_speed_data(coordinate: str, zoom: int) -> List[Dict]:
    '''
    Get speed information from TomTom api
    '''

    # Build URL
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={coordinate}&zoom={zoom}&key={apikey}"

    # Send request and parse response
    response = requests.get(url)
    # print(response)
    data = json.loads(response.text)
    traffic_flow = data["flowSegmentData"]["currentSpeed"]
    print(f"Current traffic flow: {traffic_flow} km/h")
    return data

def get_incident_data(bbox: str) -> list:
    url = f"https://api.tomtom.com/traffic/services/5/incidentDetails?key={apikey}&bbox={bbox}&language=en-GB&t=1111&timeValidityFilter=present"
    # Send request and parse response
    response = requests.get(url)
    # print(response)
    data = json.loads(response.text)
    print(data)
    accidents = data["incidents"]

    # Print accident details
    for accident in accidents:
        print(f"Type: {accident['type']}")
        # print(f"Description: {accident['text']}")
        # print(f"Location: {accident['from']} to {accident['to']}")
        print(f"Location: {accident['geometry']['coordinates']}")
    return data