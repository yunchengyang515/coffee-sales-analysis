# Databricks Learning Guide: Coffee Shop Sales Analysis

## Overview

This guide walks you through setting up Databricks Community Edition and analyzing coffee shop sales data to inform your future coffee business.

## Learning Sequence

| Phase | Focus | Skills |
|-------|-------|--------|
| 1 | Setup & Load Data | Databricks environment, file uploads, data ingestion |
| 2 | Exploratory Analysis (Python) | PySpark DataFrames, pandas, data profiling |
| 3 | Pipeline Design & Implementation | Delta Lake, data transformations, medallion architecture |
| 4 | Business Questions (SQL) | SQL analytics, dashboards, insights |

---

## Dataset Schemas

### Dataset 1: Coffee Shop Sales
**Source:** [Kaggle - Coffee Shop Sales](https://www.kaggle.com/datasets/ahmedmohamedibrahim1/coffee-shop-sales-dataset)

| Column | Type | Description |
|--------|------|-------------|
| Transaction ID | Integer | Unique transaction identifier |
| Transaction Date | Date | Date of sale |
| Transaction Time | Time | Time of sale |
| Store Number | Integer | Store identifier |
| Store Location | String | Store location name |
| Unit Number | Integer | Unit within store |
| Product Category | String | Category (e.g., Coffee, Tea) |
| Product Type | String | Product subcategory |
| Product Name | String | Specific product name |
| Price | Decimal | Sale price |
| Month | Integer | Month (1-12) |
| Day | Integer | Day of month |
| Weekday | String | Day name |
| Hour | Integer | Hour of day (0-23) |

### Dataset 2: Coffee Reviews
**Source:** [Kaggle - Coffee Reviews](https://www.kaggle.com/datasets/schmoyote/coffee-reviews-dataset)

| Column | Type | Description |
|--------|------|-------------|
| name | String | Coffee blend name |
| roaster | String | Roaster company name |
| roast | String | Roast level (Light, Medium-Light, Medium, Medium-Dark, Dark) |
| loc_country | String | Roaster's country |
| origin_1 | String | Primary bean origin |
| origin_2 | String | Secondary bean origin |
| 100g_USD | Float | Price per 100g in USD |
| rating | Float | Expert rating score |
| review_date | Date | Date of review |
| desc_1 | String | Tasting note 1 |
| desc_2 | String | Tasting note 2 |
| desc_3 | String | Tasting note 3 |

---

# Phase 1: Setup & Load Data

## Step 1.1: Set Up Databricks Community Edition

1. Go to [community.cloud.databricks.com](https://community.cloud.databricks.com/login.html)
2. Click **Sign Up** and create an account (free)
3. Verify your email
4. Log in to your workspace

**What you get:**
- 15GB storage
- Single node cluster
- Full notebook functionality
- Community support

## Step 1.2: Download the Datasets

### Sales Dataset
1. Visit [Coffee Shop Sales](https://www.kaggle.com/datasets/ahmedmohamedibrahim1/coffee-shop-sales-dataset)
2. Click **Download** (requires free Kaggle account)
3. Unzip the downloaded file

### Reviews Dataset
1. Visit [Coffee Reviews](https://www.kaggle.com/datasets/schmoyote/coffee-reviews-dataset)
2. Click **Download**
3. Unzip - use `coffee_analysis.csv` for more data

## Step 1.3: Upload Data to Databricks

**IMPORTANT:** Databricks Community Edition has disabled public DBFS. You MUST use Unity Catalog Volumes.

### Create a Volume and Upload Files

1. In Databricks sidebar, click **Catalog**
2. Navigate to: `main` > `default`
3. Click **Create** > **Volume**
4. Name it `raw_data`, click **Create**
5. Click on the volume name to open it
6. Click **Upload** to upload your files
7. Your file path will be: `/Volumes/main/default/raw_data/your_file_name`

### For Excel Files (.xlsx)

**Easiest approach:** Use the Databricks UI to create a table directly:
1. In **Catalog**, click **+** > **Add data**
2. Upload your `.xlsx` file
3. Databricks will auto-detect the schema
4. Name the table `coffee_sales_raw`
5. Now you can access it as `main.default.coffee_sales_raw`

## Step 1.4: Create Your First Cluster

1. Click **Compute** in the sidebar
2. Click **Create Compute**
3. Settings:
   - Name: `coffee-analysis`
   - Runtime: Latest LTS version
   - Node type: Smallest available
4. Click **Create Compute**
5. Wait for cluster to start (green circle)

## Step 1.5: Create Analysis Notebook

1. Click **+ New** > **Notebook**
2. Name: `01_Exploratory_Analysis`
3. Default language: **Python**
4. Cluster: Select `coffee-analysis`

## Step 1.6: Load the Data

### If you created a table via UI:

```python
# Load from the table you created
df = spark.table("main.default.coffee_sales_raw")
display(df)
```

### If you uploaded a CSV to a Volume:

```python
# Load CSV from Volume
FILE_PATH = "/Volumes/main/default/raw_data/Coffee Shop Sales.csv"

df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(FILE_PATH)

display(df)
```

### If you have an Excel file in a Volume:

```python
# For Excel files, use pandas
import pandas as pd

FILE_PATH = "/Volumes/main/default/raw_data/Coffee Shop Sales.xlsx"

pandas_df = pd.read_excel(FILE_PATH)
df = spark.createDataFrame(pandas_df)

display(df)
```

---

# Phase 2: Exploratory Analysis (Python)

## Step 2.1: Understand the Data Structure

```python
# Check schema
df.printSchema()
```

```python
# Row count
print(f"Total rows: {df.count():,}")
print(f"Total columns: {len(df.columns)}")
```

```python
# Column names
df.columns
```

## Step 2.2: Basic Statistics

```python
# Summary statistics for all columns
display(df.describe())
```

```python
# For specific numeric column
display(df.select("Price").summary())
```

## Step 2.3: Check Data Quality

```python
from pyspark.sql.functions import col, count, when, isnull

# Count nulls per column
null_counts = df.select([
    count(when(isnull(c), c)).alias(c)
    for c in df.columns
])

display(null_counts)
```

```python
# Check for duplicates
total = df.count()
distinct = df.distinct().count()
print(f"Total rows: {total:,}")
print(f"Distinct rows: {distinct:,}")
print(f"Duplicate rows: {total - distinct:,}")
```

## Step 2.4: Explore Categorical Columns

```python
# Unique values in Store Location
display(df.select("Store Location").distinct())
```

```python
# Value counts for Product Category
display(
    df.groupBy("Product Category")
    .count()
    .orderBy("count", ascending=False)
)
```

```python
# Explore Product Types within each Category
display(
    df.groupBy("Product Category", "Product Type")
    .count()
    .orderBy("Product Category", "count", ascending=[True, False])
)
```

## Step 2.5: Explore Numeric Distributions

```python
from pyspark.sql.functions import min, max, avg, stddev, percentile_approx

# Price distribution
display(
    df.select(
        min("Price").alias("min"),
        percentile_approx("Price", 0.25).alias("p25"),
        percentile_approx("Price", 0.5).alias("median"),
        percentile_approx("Price", 0.75).alias("p75"),
        max("Price").alias("max"),
        avg("Price").alias("mean"),
        stddev("Price").alias("std")
    )
)
```

```python
# Price histogram data
display(
    df.select("Price")
    .withColumn("price_bucket", (col("Price") / 1).cast("int"))
    .groupBy("price_bucket")
    .count()
    .orderBy("price_bucket")
)
```

## Step 2.6: Time-Based Exploration

```python
# Transactions by hour
display(
    df.groupBy("Hour")
    .count()
    .orderBy("Hour")
)
```

```python
# Transactions by day of week
display(
    df.groupBy("Weekday")
    .count()
)
```

```python
# Transactions by month
display(
    df.groupBy("Month")
    .count()
    .orderBy("Month")
)
```

## Step 2.7: Using Pandas for Quick Analysis

```python
# Convert to pandas for more flexible analysis (for smaller datasets)
pdf = df.toPandas()
```

```python
# Quick pandas profiling
pdf.info()
```

```python
# Correlation matrix (numeric columns only)
pdf.select_dtypes(include=['number']).corr()
```

```python
# Value counts
pdf["Product Category"].value_counts()
```

## Step 2.8: Document Your Findings

Create a summary cell:

```python
# EDA Summary
print("=" * 50)
print("EXPLORATORY DATA ANALYSIS SUMMARY")
print("=" * 50)
print(f"Date Range: {df.select(min('Transaction Date')).collect()[0][0]} to {df.select(max('Transaction Date')).collect()[0][0]}")
print(f"Total Transactions: {df.count():,}")
print(f"Total Revenue: ${df.agg({'Price': 'sum'}).collect()[0][0]:,.2f}")
print(f"Locations: {df.select('Store Location').distinct().count()}")
print(f"Products: {df.select('Product Name').distinct().count()}")
print(f"Categories: {df.select('Product Category').distinct().count()}")
print("=" * 50)
```

---

# Phase 3: Pipeline Design & Implementation

## Step 3.1: Understanding the Medallion Architecture

```
Bronze (Raw)     →    Silver (Cleaned)    →    Gold (Business)
─────────────────────────────────────────────────────────────
Raw ingested         Cleaned, validated       Aggregated,
data as-is           standardized types       business-ready
```

## Step 3.2: Create Bronze Layer (Raw Data)

```python
# Save raw data to Delta Lake (Bronze layer)
df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("main.default.bronze_coffee_sales")

print("Bronze table created!")
```

## Step 3.3: Create Silver Layer (Cleaned Data)

```python
from pyspark.sql.functions import col, to_date, to_timestamp, trim, lower

# Read from bronze
bronze_df = spark.table("main.default.bronze_coffee_sales")

# Clean and transform
silver_df = bronze_df \
    .withColumn("transaction_id", col("Transaction ID").cast("integer")) \
    .withColumn("transaction_date", to_date(col("Transaction Date"), "yyyy-MM-dd")) \
    .withColumn("store_location", trim(col("Store Location"))) \
    .withColumn("product_category", trim(col("Product Category"))) \
    .withColumn("product_type", trim(col("Product Type"))) \
    .withColumn("product_name", trim(col("Product Name"))) \
    .withColumn("price", col("Price").cast("decimal(10,2)")) \
    .withColumn("hour", col("Hour").cast("integer")) \
    .withColumn("month", col("Month").cast("integer")) \
    .withColumn("day", col("Day").cast("integer")) \
    .withColumn("weekday", trim(col("Weekday"))) \
    .select(
        "transaction_id",
        "transaction_date",
        "store_location",
        "product_category",
        "product_type",
        "product_name",
        "price",
        "hour",
        "month",
        "day",
        "weekday"
    )

# Remove nulls in critical columns
silver_df = silver_df.dropna(subset=["transaction_id", "price", "product_name"])

# Save to Silver
silver_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("main.default.silver_coffee_sales")

print(f"Silver table created with {silver_df.count():,} rows")
```

## Step 3.4: Create Gold Layer (Business Aggregations)

### Gold Table: Daily Sales Summary

```python
from pyspark.sql.functions import sum, count, avg, countDistinct

silver_df = spark.table("main.default.silver_coffee_sales")

# Daily aggregation
gold_daily = silver_df.groupBy("transaction_date", "store_location") \
    .agg(
        count("*").alias("total_transactions"),
        sum("price").alias("total_revenue"),
        avg("price").alias("avg_transaction_value"),
        countDistinct("product_name").alias("unique_products_sold")
    )

gold_daily.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("main.default.gold_daily_sales")

print("Gold daily sales table created!")
```

### Gold Table: Product Performance

```python
# Product-level aggregation
gold_products = silver_df.groupBy("product_category", "product_type", "product_name") \
    .agg(
        count("*").alias("units_sold"),
        sum("price").alias("total_revenue"),
        avg("price").alias("avg_price")
    )

gold_products.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("main.default.gold_product_performance")

print("Gold product performance table created!")
```

### Gold Table: Hourly Patterns

```python
# Hourly patterns by location
gold_hourly = silver_df.groupBy("store_location", "hour", "weekday") \
    .agg(
        count("*").alias("transactions"),
        sum("price").alias("revenue")
    )

gold_hourly.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("main.default.gold_hourly_patterns")

print("Gold hourly patterns table created!")
```

## Step 3.5: Verify Your Pipeline

```python
# List all tables you created
display(spark.sql("SHOW TABLES IN main.default"))
```

```python
# Check row counts
print("Pipeline Summary:")
print(f"Bronze: {spark.table('main.default.bronze_coffee_sales').count():,} rows")
print(f"Silver: {spark.table('main.default.silver_coffee_sales').count():,} rows")
print(f"Gold Daily: {spark.table('main.default.gold_daily_sales').count():,} rows")
print(f"Gold Products: {spark.table('main.default.gold_product_performance').count():,} rows")
print(f"Gold Hourly: {spark.table('main.default.gold_hourly_patterns').count():,} rows")
```

---

# Phase 4: Business Questions (SQL)

Create a new notebook: `02_Business_Analysis_SQL`

Now that your pipeline is built, use SQL to answer business questions!

## Step 4.1: Verify Tables Exist

```sql
%sql
SHOW TABLES IN main.default LIKE 'gold*'
```

## Step 4.2: Executive Summary

```sql
%sql
-- Key business metrics
SELECT
    COUNT(*) as total_transactions,
    ROUND(SUM(price), 2) as total_revenue,
    ROUND(AVG(price), 2) as avg_transaction_value,
    COUNT(DISTINCT store_location) as num_locations,
    COUNT(DISTINCT product_name) as num_products,
    MIN(transaction_date) as date_from,
    MAX(transaction_date) as date_to
FROM main.default.silver_coffee_sales
```

## Step 4.3: Peak Hours Analysis

```sql
%sql
-- When are peak hours? (for staffing decisions)
SELECT
    hour,
    COUNT(*) as transactions,
    ROUND(SUM(price), 2) as revenue,
    ROUND(AVG(price), 2) as avg_transaction
FROM main.default.silver_coffee_sales
GROUP BY hour
ORDER BY hour
```

## Step 4.4: Day of Week Patterns

```sql
%sql
-- Weekday vs weekend patterns
SELECT
    weekday,
    COUNT(*) as transactions,
    ROUND(SUM(price), 2) as revenue,
    CASE weekday
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END as day_order
FROM main.default.silver_coffee_sales
GROUP BY weekday
ORDER BY day_order
```

## Step 4.5: Product Category Performance

```sql
%sql
-- What categories drive the business?
SELECT
    product_category,
    units_sold,
    ROUND(total_revenue, 2) as total_revenue,
    ROUND(avg_price, 2) as avg_price,
    ROUND(total_revenue * 100.0 / SUM(total_revenue) OVER(), 1) as revenue_share_pct
FROM main.default.gold_product_performance
GROUP BY product_category, units_sold, total_revenue, avg_price
ORDER BY total_revenue DESC
```

## Step 4.6: Top 10 Products by Revenue

```sql
%sql
-- Which products are money makers?
SELECT
    product_name,
    product_category,
    units_sold,
    ROUND(total_revenue, 2) as total_revenue
FROM main.default.gold_product_performance
ORDER BY total_revenue DESC
LIMIT 10
```

## Step 4.7: Location Comparison

```sql
%sql
-- Which locations perform best?
SELECT
    store_location,
    SUM(total_transactions) as transactions,
    ROUND(SUM(total_revenue), 2) as total_revenue,
    ROUND(AVG(avg_transaction_value), 2) as avg_transaction_value
FROM main.default.gold_daily_sales
GROUP BY store_location
ORDER BY total_revenue DESC
```

## Step 4.8: Product Preferences by Location

```sql
%sql
-- Top 3 categories per location
WITH location_category AS (
    SELECT
        store_location,
        product_category,
        SUM(price) as revenue,
        ROW_NUMBER() OVER (PARTITION BY store_location ORDER BY SUM(price) DESC) as rank
    FROM main.default.silver_coffee_sales
    GROUP BY store_location, product_category
)
SELECT * FROM location_category
WHERE rank <= 3
ORDER BY store_location, rank
```

## Step 4.9: Monthly Trends

```sql
%sql
-- Month over month performance
SELECT
    month,
    COUNT(*) as transactions,
    ROUND(SUM(price), 2) as revenue,
    ROUND(AVG(price), 2) as avg_transaction
FROM main.default.silver_coffee_sales
GROUP BY month
ORDER BY month
```

## Step 4.10: Basket Size Analysis

```sql
%sql
-- How many items per transaction?
WITH baskets AS (
    SELECT
        transaction_id,
        COUNT(*) as items,
        SUM(price) as basket_total
    FROM main.default.silver_coffee_sales
    GROUP BY transaction_id
)
SELECT
    ROUND(AVG(items), 2) as avg_items_per_transaction,
    ROUND(AVG(basket_total), 2) as avg_basket_value,
    MAX(items) as max_items,
    ROUND(MAX(basket_total), 2) as max_basket_value
FROM baskets
```

## Step 4.11: Hourly Revenue Heatmap by Location

```sql
%sql
-- Revenue by location and hour (for heatmap visualization)
SELECT
    store_location,
    hour,
    SUM(transactions) as total_transactions,
    ROUND(SUM(revenue), 2) as total_revenue
FROM main.default.gold_hourly_patterns
GROUP BY store_location, hour
ORDER BY store_location, hour
```

---

# Checklist

### Phase 1: Setup
- [ ] Created Databricks Community Edition account
- [ ] Downloaded datasets from Kaggle
- [ ] Created Volume and uploaded data
- [ ] Created and started cluster
- [ ] Successfully loaded data into DataFrame

### Phase 2: Exploratory Analysis
- [ ] Checked schema and data types
- [ ] Analyzed data quality (nulls, duplicates)
- [ ] Explored categorical distributions
- [ ] Explored numeric distributions
- [ ] Documented findings

### Phase 3: Pipeline
- [ ] Created Bronze table (raw data)
- [ ] Created Silver table (cleaned data)
- [ ] Created Gold tables (aggregations)
- [ ] Verified pipeline

### Phase 4: Business Analysis
- [ ] Executive summary metrics
- [ ] Peak hours analysis
- [ ] Product performance
- [ ] Location comparison
- [ ] Documented insights in [STRATEGY.md](STRATEGY.md)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cluster won't start | Wait 5 min, or delete and recreate |
| File not found | Check path in Catalog > Volumes |
| DBFS disabled error | Use Unity Catalog Volumes instead |
| Excel file won't load | Use pandas: `pd.read_excel()` |
| Schema issues | Use `.option("inferSchema", "false")` and cast manually |
| Session expired | Re-attach notebook to cluster |

---

## Resources

- [Databricks Documentation](https://docs.databricks.com/)
- [PySpark DataFrame Guide](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html)
- [Delta Lake Guide](https://docs.delta.io/latest/index.html)
- [Databricks Community Forum](https://community.databricks.com/)
