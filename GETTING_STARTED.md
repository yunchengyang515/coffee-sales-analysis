# Coffee Sales Analysis - Getting Started Guide

This guide will help you get started with the Coffee Sales Analysis project.

## Quick Start (5 minutes)

### Step 1: Set Up Environment

```bash
# Clone the repository
git clone https://github.com/yunchengyang515/coffee-sales-analysis.git
cd coffee-sales-analysis

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Download Dataset

You have two options:

**Option A: Using Kaggle API (Recommended)**
```bash
# Install Kaggle
pip install kaggle

# Set up Kaggle credentials (get from https://www.kaggle.com/settings)
# Place kaggle.json in ~/.kaggle/

# Download dataset
kaggle datasets download -d ahmedmohamedibrahim1/coffee-shop-sales-dataset -p data/raw/ --unzip
```

**Option B: Manual Download**
1. Go to https://www.kaggle.com/datasets/ahmedmohamedibrahim1/coffee-shop-sales-dataset
2. Click "Download"
3. Extract the files to `data/raw/` directory

### Step 3: Run the Pipeline

```bash
# Run the complete ETL pipeline
python run_pipeline.py
```

This will:
1. Extract data (show download instructions if not present)
2. Transform and clean the data
3. Load the data (to files and optionally database)
4. Perform data quality checks

### Step 4: Analyze the Data

Choose your preferred analysis method:

**Option A: Jupyter Notebooks (Interactive)**
```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

**Option B: PySpark (Big Data)**
```bash
python scripts/spark_processing.py
```

**Option C: SQL (Database)**
```bash
# First, set up database (update credentials in config/config.yaml)
psql -U postgres -d coffee_sales_db -f sql/schema.sql

# Run analytics queries
psql -U postgres -d coffee_sales_db -f sql/analytics_queries.sql
```

## Detailed Workflow

### 1. Data Engineering Pipeline

The ETL pipeline consists of three main stages:

#### Extract (`scripts/01_extract.py`)
- Downloads data from Kaggle
- Validates data files
- Prepares for transformation

#### Transform (`scripts/02_transform.py`)
- Cleans data (removes duplicates, handles missing values)
- Parses dates and creates time features
- Validates data types
- Saves in multiple formats (CSV, Parquet)

#### Load (`scripts/03_load.py`)
- Loads data to PostgreSQL database (optional)
- Creates optimized storage formats
- Prepares data for analysis

### 2. Data Quality

Run quality checks:
```bash
python scripts/data_quality_check.py
```

Checks performed:
- **Completeness**: Missing value analysis
- **Uniqueness**: Duplicate detection
- **Validity**: Data type and range validation
- **Consistency**: Cross-field validation

### 3. Big Data Processing

Process with Apache Spark:
```bash
python scripts/spark_processing.py
```

Features:
- Distributed computing
- Advanced aggregations
- Time series analysis
- Window functions
- Performance optimization

### 4. Analytics

#### Jupyter Notebooks

**Exploratory Data Analysis**
```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

Includes:
- Data overview and statistics
- Distribution analysis
- Correlation analysis
- Visualizations

**Spark Analysis**
```bash
jupyter notebook notebooks/02_spark_analysis.ipynb
```

Includes:
- Spark-based analytics
- Large-scale aggregations
- Advanced transformations

#### SQL Analytics

Pre-built queries in `sql/analytics_queries.sql`:
- Sales trends (daily, weekly, monthly)
- Product performance
- Customer analytics
- Revenue analysis
- Cohort analysis

### 5. Database Setup (Optional)

If you want to use PostgreSQL:

1. **Install PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql
   
   # Mac with Homebrew
   brew install postgresql
   ```

2. **Create Database**
   ```bash
   psql -U postgres
   CREATE DATABASE coffee_sales_db;
   \q
   ```

3. **Update Configuration**
   Edit `config/config.yaml` with your database credentials:
   ```yaml
   database:
     host: "localhost"
     port: 5432
     database: "coffee_sales_db"
     user: "your_username"
     password: "your_password"
   ```

4. **Create Schema**
   ```bash
   psql -U postgres -d coffee_sales_db -f sql/schema.sql
   ```

5. **Load Data**
   ```bash
   python scripts/03_load.py
   ```

## Configuration

The main configuration file is `config/config.yaml`. You can customize:

- **Data Paths**: Where to store raw, cleaned, and processed data
- **Database Settings**: Connection details for PostgreSQL
- **Spark Settings**: Memory allocation and parallelism
- **Analytics Settings**: Date ranges, top N settings

## Common Issues & Solutions

### Issue: Kaggle API not working
**Solution**: 
1. Ensure `kaggle.json` is in `~/.kaggle/`
2. Set permissions: `chmod 600 ~/.kaggle/kaggle.json`
3. Check credentials at https://www.kaggle.com/settings

### Issue: PySpark not working
**Solution**:
1. Install Java 8+: `sudo apt-get install openjdk-8-jdk`
2. Set JAVA_HOME: `export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64`

### Issue: Database connection fails
**Solution**:
1. Verify PostgreSQL is running: `sudo service postgresql status`
2. Check credentials in `config/config.yaml`
3. Ensure database exists: `psql -l`

### Issue: Memory errors with Spark
**Solution**:
1. Reduce memory settings in `config/config.yaml`
2. Process data in smaller chunks
3. Use `.limit()` for testing

## Project Outputs

After running the pipeline, you'll have:

1. **Cleaned Data**: `data/cleaned/`
   - CSV and Parquet formats
   - Ready for analysis

2. **Processed Data**: `data/processed/`
   - Spark-processed data
   - Optimized for analytics

3. **Database Tables**: (if using PostgreSQL)
   - `coffee_sales`: Main fact table
   - Supporting dimension tables
   - Pre-built views

4. **Analysis Results**: Jupyter notebooks with:
   - Visualizations
   - Statistical insights
   - Business recommendations

## Next Steps for Learning

1. **Data Engineering**:
   - Modify ETL scripts for custom transformations
   - Add error handling and logging
   - Implement data versioning

2. **Big Data**:
   - Experiment with different Spark configurations
   - Try processing larger datasets
   - Implement advanced window functions

3. **Analytics**:
   - Create custom SQL queries
   - Build dashboards (Streamlit/Dash)
   - Develop predictive models

4. **DevOps**:
   - Add automated testing
   - Set up CI/CD pipeline
   - Deploy to cloud (AWS/Azure/GCP)

## Resources

- [Kaggle Dataset](https://www.kaggle.com/datasets/ahmedmohamedibrahim1/coffee-shop-sales-dataset)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Review the configuration in `config/config.yaml`
3. Ensure all dependencies are installed
4. Open an issue in the GitHub repository

---

Happy analyzing! 🚀
