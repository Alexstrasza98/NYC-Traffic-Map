import asyncio
import os

import aiohttp
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf

from apis import (
    get_incident_data,
    get_traffic_data,
    get_traffic_data_async,
    get_weather_data_async,
)
from utils import write_json

load_dotenv()

API_KEY = os.getenv("TOMTOM_API_KEY")


def get_data_async(sc):
    text_file = sc.read.text("data/coordinates_columbia.txt")
    print("Requesting traffic data...")

    loop = asyncio.new_event_loop()
    res = loop.run_until_complete(get_traffic_data_async(text_file.rdd, "15"))
    loop.close()
    return res


def get_incident_middlefile():
    print("Requesting incident data...")
    bbox = "-73.992221,40.780339,-73.933464,40.807713"
    incident_data = get_incident_data(bbox)
    return incident_data


def get_weather_async(sc):
    print("Requesting weather data...")
    text_weather_file = sc.read.text("data/coordinates_columbia.txt")
    weather_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(weather_loop)
    res_weather = weather_loop.run_until_complete(
        get_weather_data_async(text_weather_file.rdd)
    )
    weather_loop.close()
    return res_weather
