import pytest
from pyspark.sql import SparkSession

from pyspark_job import clean_data

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("PySparkTests")
        .getOrCreate()
    )

    yield spark

    spark.stop()


def test_valid_records_are_kept(spark):
    data = [
        (1, "Alice", 100.0),
        (2, "Bob", 50.0),
    ]

    df = spark.createDataFrame(data, ["id", "name", "amount"])

    result = clean_data(df)

    ids = [row.id for row in result.select("id").collect()]

    assert ids == [1, 2]


def test_non_positive_amounts_are_removed(spark):
    data = [
        (1, "Alice", 100.0),
        (2, "Bob", 0.0),
        (3, "Charlie", -20.0),
    ]

    df = spark.createDataFrame(data, ["id", "name", "amount"])

    result = clean_data(df)

    ids = [row.id for row in result.select("id").collect()]

    assert ids == [1]


def test_null_names_are_removed(spark):
    data = [
        (1, "Alice", 100.0),
        (2, None, 50.0),
    ]

    df = spark.createDataFrame(data, ["id", "name", "amount"])

    result = clean_data(df)

    ids = [row.id for row in result.select("id").collect()]

    assert ids == [1]


def test_amount_with_tax_is_calculated_correctly(spark):
    data = [
        (1, "Alice", 100.0),
        (2, "Bob", 50.0),
    ]

    df = spark.createDataFrame(data, ["id", "name", "amount"])

    result = clean_data(df)

    rows = result.select("amount_with_tax").collect()

    assert rows[0].amount_with_tax == pytest.approx(120.0)
    assert rows[1].amount_with_tax == pytest.approx(60.0)