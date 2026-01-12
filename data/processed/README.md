# Processed Data Directory

This directory contains processed data ready for analysis and reporting.

## Contents

After running the loading script (`scripts/03_load.py`) or Spark processing (`scripts/spark_processing.py`), this directory will contain:
- Parquet files optimized for big data analytics
- Aggregated datasets
- Spark-processed results

## Format

Data is stored in Parquet format for:
- Efficient storage (columnar format)
- Fast read/write operations
- Better compression
- Schema preservation

## Usage

### With Pandas:
```python
import pandas as pd
df = pd.read_parquet('data/processed/coffee_sales_processed_YYYYMMDD.parquet')
```

### With PySpark:
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
df = spark.read.parquet('data/processed/spark_processed')
```

## Note

Processed data files are excluded from git to keep the repository size manageable.
