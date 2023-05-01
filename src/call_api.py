from utils import write_json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
import asyncio
import os
import aiohttp
from tomtom import get_traffic_data, get_incident_data, get_traffic_data_async

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TomTomAPIKey")

def get_data_async(sc):
    text_file = sc.read.text("../data/coord_manhatan_test.txt")
    print("Requesting traffic data...")
    import asyncio
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(get_traffic_data_async(text_file.rdd, "15", API_KEY))
    loop.close()
    print(res)
    print(type(res))
    return res



if __name__ == "__main__":
    # trying to get the request and data loading part into pyspark session
    spark_txt = SparkSession.builder.appName("ReadCoordFile").getOrCreate()
    text_file = spark_txt.read.text("../data/coord_manhatan_test.txt")
    print("Requesting traffic data...")
    import asyncio

    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(get_traffic_data_async(text_file.rdd, "15", API_KEY))
    loop.close()
    # for line in text_file.rdd.map(lambda row: row[0]).collect():
        # print(type(line))
        # print(line)













    # with open("./data/coordinates_manhattan.txt", "r") as f:
    #     coordinates = f.readlines()

    #
    # coordinates = [coordinate.strip() for coordinate in coordinates]
    # zoom = 15
    #
    # # Only fetch first 1000 samples
    # traffic_data = get_traffic_data(coordinates[:1000], zoom)
    # write_json(traffic_data, "./data/traffic_tomtom.json")
    #
    # print("Requesting incident data...")
    # bbox = "-74.010626,40.744806,-73.960532,40.756587"
    # incident_data = get_incident_data(bbox)
    # write_json(incident_data, "./data/incident_tomtom.json")