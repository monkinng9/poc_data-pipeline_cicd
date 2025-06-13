import unittest
import os
import shutil
import logging
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType

# Adjust the import path to correctly locate the etl_process function
from app.etl_process import etl_process

# Configure logging for tests
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TestETLProcess(unittest.TestCase):
    """
    Test suite for the PySpark ETL process.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initializes a SparkSession for the test suite.
        """
        cls.spark = SparkSession.builder \
            .appName("PySparkETLTests") \
            .master("local[2]") \
            .config("spark.sql.shuffle.partitions", "1") \
            .getOrCreate()
        logging.info("SparkSession initialized for testing.")

    @classmethod
    def tearDownClass(cls):
        """
        Stops the SparkSession after all tests are completed.
        """
        cls.spark.stop()
        logging.info("SparkSession stopped.")

    def setUp(self):
        """
        Sets up temporary directories for test input and output.
        """
        self.input_path = "/tmp/test_input"
        self.output_path = "/tmp/test_output"
        os.makedirs(self.input_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)

    def tearDown(self):
        """
        Cleans up temporary directories after each test.
        """
        shutil.rmtree(self.input_path)
        shutil.rmtree(self.output_path)

    def _assert_dataframes_equal(self, df1, df2):
        """
        Asserts that two DataFrames have the same schema and content.
        """
        self.assertEqual(df1.schema, df2.schema, "DataFrame schemas do not match.")
        self.assertEqual(df1.count(), df2.count(), "DataFrame row counts do not match.")
        self.assertEqual(sorted(df1.collect()), sorted(df2.collect()), "DataFrame content does not match.")

    def test_etl_with_valid_data(self):
        """
        Tests the ETL process with a typical dataset where some rows should be filtered.
        """
        logging.info("Running test: test_etl_with_valid_data")
        # Arrange: Create test data and expected output
        input_data = [
            ("Alice", 25, "New York"),
            ("Bob", 35, "London"),
            ("Charlie", 40, "Paris")
        ]
        input_schema = StructType([
            StructField("name", StringType(), True),
            StructField("age", LongType(), True),
            StructField("city", StringType(), True)
        ])
        input_df = self.spark.createDataFrame(input_data, input_schema)
        input_df.write.mode("overwrite").csv(os.path.join(self.input_path, "input.csv"), header=True)

        expected_data = [("Bob", 35, "London"), ("Charlie", 40, "Paris")]
        expected_df = self.spark.createDataFrame(expected_data, input_schema)

        # Act: Run the ETL process
        etl_process(self.spark, os.path.join(self.input_path, "input.csv"), self.output_path)
        result_df = self.spark.read.parquet(self.output_path)

        # Assert: Check if the output matches the expected result
        self._assert_dataframes_equal(result_df, expected_df)

    def test_etl_with_empty_input(self):
        """
        Tests the ETL process with an empty input file to ensure it handles no-data scenarios gracefully.
        """
        logging.info("Running test: test_etl_with_empty_input")
        # Arrange: Create an empty file with a header
        schema = StructType([
            StructField("name", StringType(), True),
            StructField("age", LongType(), True),
            StructField("city", StringType(), True)
        ])
        empty_df = self.spark.createDataFrame([], schema)
        empty_df.write.mode("overwrite").csv(os.path.join(self.input_path, "empty.csv"), header=True)

        # Act: Run the ETL process
        etl_process(self.spark, os.path.join(self.input_path, "empty.csv"), self.output_path)
        result_df = self.spark.read.parquet(self.output_path)

        # Assert: The output should be an empty DataFrame
        self.assertEqual(result_df.count(), 0, "Output DataFrame should be empty for empty input.")

    def test_etl_no_rows_matching_filter(self):
        """
        Tests the ETL process when no rows meet the filter criteria.
        """
        logging.info("Running test: test_etl_no_rows_matching_filter")
        # Arrange: Create data where no 'age' is > 30
        input_data = [
            ("Alice", 25, "New York"),
            ("David", 30, "Berlin")
        ]
        schema = StructType([
            StructField("name", StringType(), True),
            StructField("age", LongType(), True),
            StructField("city", StringType(), True)
        ])
        input_df = self.spark.createDataFrame(input_data, schema)
        input_df.write.mode("overwrite").csv(os.path.join(self.input_path, "input.csv"), header=True)

        # Act: Run the ETL process
        etl_process(self.spark, os.path.join(self.input_path, "input.csv"), self.output_path)
        result_df = self.spark.read.parquet(self.output_path)

        # Assert: The output should be an empty DataFrame
        self.assertEqual(result_df.count(), 0, "Output should be empty when no rows match the filter.")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)