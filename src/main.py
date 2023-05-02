import os
from glob import glob

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    col,
    mean,
    monotonically_increasing_id,
    to_json,
    udf,
)

from congestion_model import generate_congestion_level, simple_congestion_model
from utils import modify_json


def run_spark_app():
    """
    Main function to run spark app, reading in speed info and writing congestion info into database
    """
    spark = (
        SparkSession.builder.master("local[*]").appName("NYC-Traffic-Map").getOrCreate()
    )

    # 1st step
    # spark reading in speed information get from TomTom API
    # TODO: figure out if we can request data from TomTom API and send to Spark directly,
    # or if we need to save the data first (file or database...)
    speed_df = spark.read.option("multiline", "true").json("data/traffic_tomtom.json")
    incident_df = spark.read.option("multiline", "true").json(
        "data/incident_tomtom.json"
    )
    weather_df = spark.read.option("multiline", "true").json("data/weather.json")

    ## 2nd step - spark processing
    ## Traffic data
    # get sample-level congestion level
    congestion_udf = udf(generate_congestion_level)
    speed_df = speed_df.withColumn(
        "congestion_level",
        congestion_udf(col("roadClosure"), col("freeFlowSpeed"), col("currentSpeed")),
    )
    speed_df = speed_df.withColumn("index", monotonically_increasing_id() + 1)
    congestion_df = speed_df.select("index", "congestion_level", "coordinates")

    # get congestion level distribution
    congestion_dist = congestion_df.groupBy("congestion_level").count()

    # get average speed and average speed percentage
    average_speed = speed_df.agg(avg("currentSpeed").alias("average_speed"))
    average_speed_percent = speed_df.select(
        col("currentSpeed") / col("freeFlowSpeed")
    ).agg(avg("(currentSpeed / freeFlowSpeed)").alias("average_speed_percent"))
    speed_statistics = average_speed.crossJoin(average_speed_percent)

    ## Incident data
    incident_dist = incident_df.groupBy("incident_type").count()

    ## Weather data
    main_weather = (
        weather_df.groupBy("weather").count().orderBy("count", ascending=False).limit(1)
    )

    avg_temp = weather_df.agg(avg("temperature").alias("average_temp"))
    avg_humidity = weather_df.agg(avg("humidity").alias("average_humidity"))
    avg_wind_speed = weather_df.agg(avg("wind_speed").alias("average_wind_speed"))
    avg_rain = weather_df.agg(avg("rain").alias("average_rain"))
    avg_visibility = weather_df.agg(avg("visibility").alias("average_visibility"))

    weather_result = (
        main_weather.select("weather")
        .crossJoin(avg_temp)
        .crossJoin(avg_humidity)
        .crossJoin(avg_wind_speed)
        .crossJoin(avg_rain)
        .crossJoin(avg_visibility)
    )

    # 3rd step - writing results to local files
    congestion_df.write.json("data/congestion/congestion_map", mode="overwrite")
    congestion_dist.write.csv(
        "data/congestion/congestion_dist", mode="overwrite", header=True
    )
    speed_statistics.write.json(
        "data/congestion/congestion_statistics", mode="overwrite"
    )

    incident_df.write.json("data/incident/incident_map", mode="overwrite")
    incident_dist.write.csv(
        "data/incident/incident_dist", mode="overwrite", header=True
    )

    weather_result.write.json("data/weather/weather_statistics", mode="overwrite")

    # TODO: does it mean we need three processers, one for calling TomTom, one for Spark, one for frontend?
    # or we can have one processer for calling TomTom and Spark, and another processer for frontend?

    # congestion_df.awaitTermination()


def fix_file_name(folder_path, file_format):
    input_file_name = glob(os.path.join(folder_path, f"*.{file_format}"))[0]
    output_file_name = folder_path.split("/")[-1] + f".{file_format}"
    os.rename(input_file_name, os.path.join(folder_path, output_file_name))


if __name__ == "__main__":
    run_spark_app()

    # Fix output file name
    input_traffic = glob("./data/congestion/congestion_map/*.json")[0]
    output_traffic = "./data/congestion/congestion_map/congestion_map.json"
    modify_json(input_traffic, output_traffic)

    input_incident = glob("./data/incident/incident_map/*.json")[0]
    output_incicent = "./data/incident/incident_map/incident_map.json"
    modify_json(input_incident, output_incicent)

    folders_to_fix = [
        ["data/congestion/congestion_dist", "csv"],
        ["data/congestion/congestion_statistics", "json"],
        ["data/incident/incident_dist", "csv"],
        ["data/weather/weather_statistics", "json"],
    ]

    for folder_path, file_format in folders_to_fix:
        fix_file_name(folder_path, file_format)
