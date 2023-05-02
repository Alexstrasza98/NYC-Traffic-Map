import time

from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("ScheduledTaskExample").getOrCreate()


# Define a task to be scheduled
def my_task():
    print("Running my task...")
    # Perform some processing here...


# Schedule the task to run every 5 seconds
spark.sparkContext.scheduler().schedule(interval=5, action=my_task)

# Wait for the scheduled tasks to complete
time.sleep(30)

# Stop the SparkSession
spark.stop()
