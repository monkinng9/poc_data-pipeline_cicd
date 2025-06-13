import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import LongType, StructType, StructField, StringType

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def etl_process(spark: SparkSession, input_path: str, output_path: str):
    """
    Performs a simple ETL process on a PySpark DataFrame.

    This function reads data from a CSV file, ensures the 'age' column
    is of LongType for consistency, filters the DataFrame to include
    only rows where 'age' is greater than 30, and writes the
    transformed data to a Parquet file.

    Args:
        spark (SparkSession): The active SparkSession.
        input_path (str): The path to the input CSV data.
        output_path (str): The path to write the output Parquet data.

    Returns:
        DataFrame: The transformed PySpark DataFrame.

    Raises:
        Exception: If the ETL process fails at any stage.
    """
    try:
        logging.info(f"Starting ETL process from '{input_path}'...")

        # Define schema to ensure data consistency upon reading
        schema = StructType([
            StructField("name", StringType(), True),
            StructField("age", LongType(), True),  # Use LongType for consistency
            StructField("city", StringType(), True)
        ])

        # Extraction: Read data using the defined schema
        df = spark.read.csv(input_path, header=True, schema=schema)
        logging.info(f"Successfully extracted data from '{input_path}'.")

        # Transformation: Filter rows where 'age' is greater than 30
        transformed_df = df.filter(col("age") > 30)
        logging.info("Successfully transformed data by filtering based on age > 30.")

        # Loading: Write the transformed data to the output path
        transformed_df.write.mode("overwrite").parquet(output_path)
        logging.info(f"Successfully loaded transformed data to '{output_path}'.")

        return transformed_df

    except Exception as e:
        logging.error(f"ETL process failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # This block provides an example of how to run the ETL process directly.
    spark_session = SparkSession.builder \
        .appName("SimpleETLExample") \
        .master("local[*]") \
        .getOrCreate()

    # Create dummy input data for demonstration
    temp_input_path = "/tmp/input_data"
    temp_output_path = "/tmp/output_data"
    
    demo_data = [
        ("Alice", 25, "New York"),
        ("Bob", 35, "London"),
        ("Charlie", 40, "Paris"),
        ("David", 30, "Berlin")
    ]
    columns = ["name", "age", "city"]
    input_df = spark_session.createDataFrame(demo_data, columns)

    # Write dummy data to CSV
    input_df.write.mode("overwrite").csv(temp_input_path, header=True)
    print(f"Created temporary input data at: {temp_input_path}")

    # Run the ETL process
    print("Running ETL process...")
    result_df = etl_process(spark_session, temp_input_path, temp_output_path)
    
    print("ETL process completed. Resulting data:")
    result_df.show()

    spark_session.stop()