from pyspark.sql import SparkSession
from pyspark.sql.functions import udf


def simple_congestion_model(expected_speed: int, actual_speed: int) -> int:
    """
    Evalute congestion level of a road segment depending on the difference between expected and actual speed.
    This model is a naive version, which only considers the speed difference.
    Reference: https://developer.tomtom.com/traffic-api/documentation/traffic-flow/raster-flow-tiles

    Params:
        expected_speed: Expected speed of a road segment
        actual_speed: Actual speed of a road segment

    Returns:
        congestion_level: Congestion level of a road segment
    """

    speed_percentage = actual_speed / expected_speed

    assert (
        speed_percentage >= 0 and speed_percentage <= 1
    ), f"Speed percentage must be between 0 and 1, got {speed_percentage}"

    # 0 is reserved for road closed
    if speed_percentage < 0.15:
        congestion_level = 1
    elif speed_percentage < 0.35:
        congestion_level = 2
    elif speed_percentage < 0.75:
        congestion_level = 3
    else:
        congestion_level = 4

    return congestion_level


def generate_congestion_level(road_closure, free_flow_speed, current_speed):
    """
    Generate congestion level for one piece of road segment
    """

    if road_closure:
        return 0
    else:
        return simple_congestion_model(free_flow_speed, current_speed)


def run_spark_app():
    """
    Main function to run spark app, reading in speed info and writing congestion info into database
    """
    spark = (
        SparkSession.builder.master("local").appName("NYC-Traffic-Map").getOrCreate()
    )

    # 1st step
    # spark reading in speed information get from TomTom API
    # TODO: figure out if we can request data from TomTom API and send to Spark directly,
    # or if we need to save the data first (file or database...)
    speed_df = spark.read.option("multiline", "true").json("data/traffic_tomtom.json")

    # 2nd step
    # spark do processing, getting congestion level information (and other global metrics)
    congestion_udf = udf(generate_congestion_level)
    congestion_df = speed_df.select(
        congestion_udf("roadClosure", "freeFlowSpeed", "currentSpeed").alias(
            "congestion_level"
        ),
        "coordinates",
    )

    # 3rd step
    # spark write the result to database
    congestion_df.write.json("data/congestion_map")

    # TODO: does it mean we need three processers, one for calling TomTom, one for Spark, one for frontend?
    # or we can have one processer for calling TomTom and Spark, and another processer for frontend?

    # congestion_df.awaitTermination()


if __name__ == "__main__":
    run_spark_app()
