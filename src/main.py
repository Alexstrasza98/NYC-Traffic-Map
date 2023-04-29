from pyspark.sql import SparkSession
from pyspark.sql.functions import udf

from congestion_model import generate_congestion_level, simple_congestion_model


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
