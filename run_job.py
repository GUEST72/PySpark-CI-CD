from pyspark.sql import SparkSession

from pyspark_job import clean_data


spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("PySparkJob")
    .getOrCreate()
)

data = [
    (1, "Alice", 100.0),
    (2, "Bob", 50.0),
    (3, None, 20.0),
    (4, "Charlie", -10.0),
]

df = spark.createDataFrame(
    data,
    ["id", "name", "amount"]
)

result = clean_data(df)

result.show()

spark.stop()