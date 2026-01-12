"""
PySpark Big Data Processing for Coffee Sales Dataset
This script demonstrates big data processing using Apache Spark.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum as spark_sum, avg, max as spark_max, min as spark_min,
    year, month, dayofmonth, hour, dayofweek, date_format, to_date, to_timestamp
)
from pyspark.sql.window import Window
import pyspark.sql.functions as F
from pathlib import Path
import yaml


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_spark_session(config):
    """Create and configure Spark session"""
    spark_config = config['spark']
    
    spark = SparkSession.builder \
        .appName(spark_config['app_name']) \
        .master(spark_config['master']) \
        .config("spark.driver.memory", spark_config['driver_memory']) \
        .config("spark.executor.memory", spark_config['executor_memory']) \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    print(f"Spark Session created: {spark.version}")
    return spark


def load_data(spark, data_path):
    """Load data using Spark"""
    # Try to load parquet first
    parquet_files = list(data_path.glob("*.parquet"))
    
    if parquet_files:
        latest_file = str(max(parquet_files, key=lambda x: x.stat().st_mtime))
        print(f"Loading data from: {Path(latest_file).name}")
        df = spark.read.parquet(latest_file)
    else:
        # Fall back to CSV
        csv_files = list(data_path.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"No data files found in {data_path}")
        
        latest_file = str(max(csv_files, key=lambda x: x.stat().st_mtime))
        print(f"Loading data from: {Path(latest_file).name}")
        df = spark.read.csv(latest_file, header=True, inferSchema=True)
    
    print(f"Loaded {df.count()} rows")
    return df


def perform_aggregations(df):
    """Perform various aggregations for analytics"""
    print("\n" + "=" * 50)
    print("Performing Aggregations")
    print("=" * 50)
    
    # Show schema
    print("\nSchema:")
    df.printSchema()
    
    # Basic statistics
    print("\nBasic Statistics:")
    df.describe().show()
    
    # Get numeric columns for aggregation
    numeric_cols = [field.name for field in df.schema.fields 
                    if str(field.dataType) in ['IntegerType', 'DoubleType', 'FloatType', 'LongType']]
    
    if numeric_cols:
        print(f"\nAggregating numeric columns: {numeric_cols}")
        
        # Create aggregation expressions
        agg_exprs = []
        for col_name in numeric_cols[:5]:  # Limit to first 5 numeric columns
            agg_exprs.extend([
                spark_sum(col_name).alias(f"{col_name}_sum"),
                avg(col_name).alias(f"{col_name}_avg"),
                spark_max(col_name).alias(f"{col_name}_max"),
                spark_min(col_name).alias(f"{col_name}_min")
            ])
        
        df.agg(*agg_exprs).show()
    
    return df


def time_series_analysis(df):
    """Perform time series analysis"""
    print("\n" + "=" * 50)
    print("Time Series Analysis")
    print("=" * 50)
    
    # Find date/timestamp columns
    date_cols = [field.name for field in df.schema.fields 
                 if 'date' in field.name.lower() or 'time' in field.name.lower()]
    
    if not date_cols:
        print("No date columns found for time series analysis")
        return df
    
    # Use the first date column
    date_col = date_cols[0]
    print(f"\nAnalyzing time series using column: {date_col}")
    
    # Convert to timestamp if needed
    df_time = df.withColumn("timestamp", to_timestamp(col(date_col)))
    
    # Extract time components
    df_time = df_time.withColumn("year", year("timestamp")) \
                     .withColumn("month", month("timestamp")) \
                     .withColumn("day", dayofmonth("timestamp")) \
                     .withColumn("hour", hour("timestamp")) \
                     .withColumn("dayofweek", dayofweek("timestamp"))
    
    # Daily aggregation
    print("\nDaily Transaction Counts:")
    df_time.groupBy("year", "month", "day") \
           .agg(count("*").alias("transaction_count")) \
           .orderBy("year", "month", "day") \
           .show(10)
    
    # Hourly pattern
    print("\nHourly Pattern:")
    df_time.groupBy("hour") \
           .agg(count("*").alias("transaction_count")) \
           .orderBy("hour") \
           .show()
    
    # Day of week pattern
    print("\nDay of Week Pattern:")
    df_time.groupBy("dayofweek") \
           .agg(count("*").alias("transaction_count")) \
           .orderBy("dayofweek") \
           .show()
    
    return df_time


def category_analysis(df):
    """Perform categorical analysis"""
    print("\n" + "=" * 50)
    print("Category Analysis")
    print("=" * 50)
    
    # Find categorical columns (string type)
    categorical_cols = [field.name for field in df.schema.fields 
                        if str(field.dataType) == 'StringType']
    
    if not categorical_cols:
        print("No categorical columns found")
        return df
    
    # Analyze first few categorical columns
    for col_name in categorical_cols[:3]:  # Limit to first 3 categorical columns
        print(f"\nTop values in {col_name}:")
        df.groupBy(col_name) \
          .agg(count("*").alias("count")) \
          .orderBy(col("count").desc()) \
          .show(10)
    
    return df


def window_functions_example(df):
    """Demonstrate window functions for advanced analytics"""
    print("\n" + "=" * 50)
    print("Window Functions Example")
    print("=" * 50)
    
    # Find numeric columns
    numeric_cols = [field.name for field in df.schema.fields 
                    if str(field.dataType) in ['IntegerType', 'DoubleType', 'FloatType', 'LongType']]
    
    if len(numeric_cols) < 1:
        print("No numeric columns found for window functions")
        return df
    
    # Use first numeric column
    numeric_col = numeric_cols[0]
    
    # Create a window specification - use existing column if available
    # For demonstration purposes, we partition by all columns for a consistent row number
    window_spec = Window.orderBy(*df.columns[:3] if len(df.columns) >= 3 else df.columns)
    
    # Add row number and rank
    df_windowed = df.withColumn("row_number", F.row_number().over(window_spec))
    
    print(f"\nSample with row numbers:")
    df_windowed.select("row_number", *df.columns[:5]).show(10)
    
    return df_windowed


def save_results(df, output_path):
    """Save processed results"""
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save as Parquet (best for Spark)
    parquet_output = str(output_path / "spark_processed")
    df.write.mode("overwrite").parquet(parquet_output)
    print(f"\nSaved Spark processed data to: {parquet_output}")
    
    # Save as CSV (for compatibility)
    csv_output = str(output_path / "spark_processed_csv")
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(csv_output)
    print(f"Saved Spark processed data to: {csv_output}")


def main():
    """Main Spark processing pipeline"""
    print("Coffee Sales Big Data Processing with PySpark")
    print("=" * 50)
    
    config = load_config()
    project_root = Path(__file__).parent.parent
    
    # Determine input path (try processed first, then cleaned)
    processed_path = project_root / config['data']['processed_data_path']
    cleaned_path = project_root / config['data']['cleaned_data_path']
    
    if list(processed_path.glob("*.parquet")) or list(processed_path.glob("*.csv")):
        data_path = processed_path
    else:
        data_path = cleaned_path
    
    try:
        # Create Spark session
        spark = create_spark_session(config)
        
        # Load data
        df = load_data(spark, data_path)
        
        # Perform analyses
        df = perform_aggregations(df)
        df = time_series_analysis(df)
        df = category_analysis(df)
        df = window_functions_example(df)
        
        # Save results
        save_results(df, processed_path)
        
        print("\n" + "=" * 50)
        print("Big Data processing completed successfully!")
        
        # Stop Spark session
        spark.stop()
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please run the ETL pipeline first (01_extract.py, 02_transform.py, 03_load.py)")
    except Exception as e:
        print(f"\nError during Spark processing: {e}")
        raise


if __name__ == "__main__":
    main()
