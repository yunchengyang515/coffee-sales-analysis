# Coffee Sales Analysis Project

A comprehensive data engineering, analytics, and Big Data project using the Coffee Shop Sales dataset from Kaggle.

## 📊 Project Overview

This project demonstrates end-to-end data engineering practices including:
- ETL (Extract, Transform, Load) pipelines
- Data quality checks and validation
- Big Data processing with Apache Spark
- Analytics and visualization
- SQL-based reporting

## 🗂️ Dataset

**Source**: [Coffee Shop Sales Dataset on Kaggle](https://www.kaggle.com/datasets/ahmedmohamedibrahim1/coffee-shop-sales-dataset/code)

This dataset contains coffee shop sales transactions including information about products, customers, stores, and sales metrics.

## 🏗️ Project Structure

```
coffee-sales-analysis/
├── config/              # Configuration files
│   └── config.yaml      # Main configuration
├── data/                # Data directories
│   ├── raw/            # Raw data from Kaggle
│   ├── cleaned/        # Cleaned and preprocessed data
│   └── processed/      # Processed data ready for analysis
├── notebooks/          # Jupyter notebooks for analysis
│   ├── 01_exploratory_data_analysis.ipynb
│   └── 02_spark_analysis.ipynb
├── scripts/            # Python scripts for data processing
│   ├── 01_extract.py           # Data extraction
│   ├── 02_transform.py         # Data transformation
│   ├── 03_load.py              # Data loading to database
│   ├── spark_processing.py    # Big Data processing with Spark
│   └── data_quality_check.py  # Data quality validation
├── sql/                # SQL queries and schema
│   ├── schema.sql              # Database schema
│   └── analytics_queries.sql   # Analytics queries
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Java 8+ (for PySpark)
- PostgreSQL (optional, for database loading)
- Kaggle API credentials (for data download)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yunchengyang515/coffee-sales-analysis.git
   cd coffee-sales-analysis
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Kaggle API** (for dataset download)
   - Get your Kaggle API credentials from https://www.kaggle.com/settings
   - Place `kaggle.json` in `~/.kaggle/`
   - Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

5. **Update configuration**
   - Edit `config/config.yaml` with your database credentials and preferences

## 📥 Data Pipeline

### 1. Extract Data

Download the dataset from Kaggle:

```bash
# Using the script (shows download command)
python scripts/01_extract.py

# Or directly with Kaggle CLI
kaggle datasets download -d ahmedmohamedibrahim1/coffee-shop-sales-dataset -p data/raw/ --unzip
```

### 2. Transform Data

Clean and preprocess the raw data:

```bash
python scripts/02_transform.py
```

This script:
- Removes duplicates
- Handles missing values
- Parses date/time columns
- Creates time-based features
- Saves cleaned data in both CSV and Parquet formats

### 3. Load Data

Load the processed data into a database:

```bash
python scripts/03_load.py
```

This script:
- Loads cleaned data
- Connects to PostgreSQL database (optional)
- Creates tables and loads data
- Saves processed data for analysis

### 4. Data Quality Checks

Validate data quality:

```bash
python scripts/data_quality_check.py
```

Performs checks for:
- Data completeness
- Uniqueness (duplicates)
- Validity (data types, ranges)
- Consistency

### 5. Big Data Processing

Process data with Apache Spark:

```bash
python scripts/spark_processing.py
```

This demonstrates:
- Distributed data processing
- Advanced aggregations
- Time series analysis
- Window functions
- Performance optimization

## 📊 Analytics

### Jupyter Notebooks

1. **Exploratory Data Analysis**
   ```bash
   jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
   ```
   - Data overview and statistics
   - Visualizations
   - Pattern discovery

2. **Spark Analysis**
   ```bash
   jupyter notebook notebooks/02_spark_analysis.ipynb
   ```
   - Big Data processing with PySpark
   - Advanced analytics
   - Performance demonstrations

### SQL Analytics

The `sql/` directory contains:
- `schema.sql`: Database schema with tables and views
- `analytics_queries.sql`: Pre-built analytical queries for:
  - Sales trends
  - Product performance
  - Customer analytics
  - Revenue analysis
  - Time-based patterns

Example query:
```bash
psql -U postgres -d coffee_sales_db -f sql/schema.sql
psql -U postgres -d coffee_sales_db -f sql/analytics_queries.sql
```

## 🔍 Key Features

### ETL Pipeline
- ✅ Automated data extraction from Kaggle
- ✅ Comprehensive data cleaning and transformation
- ✅ Database loading with SQLAlchemy
- ✅ Support for multiple data formats (CSV, Parquet)

### Big Data Processing
- ✅ Apache Spark integration
- ✅ Distributed computing examples
- ✅ Performance optimization techniques
- ✅ Scalable data processing

### Analytics
- ✅ Statistical analysis
- ✅ Time series analysis
- ✅ Customer segmentation
- ✅ Product performance metrics
- ✅ Revenue analytics

### Data Quality
- ✅ Automated quality checks
- ✅ Data profiling
- ✅ Validation reports
- ✅ Consistency checks

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **PySpark**: Big Data processing
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Relational database
- **Jupyter**: Interactive notebooks
- **Matplotlib/Seaborn/Plotly**: Data visualization
- **PyYAML**: Configuration management

## 📈 Sample Analyses

The project includes examples of:
1. **Sales Trends**: Daily, weekly, and monthly patterns
2. **Product Analytics**: Top products, category performance
3. **Customer Insights**: Purchase frequency, customer lifetime value
4. **Time Patterns**: Peak hours, day-of-week analysis
5. **Revenue Analysis**: Store performance, basket size

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available for educational purposes.

## 📚 Learning Resources

This project demonstrates skills in:
- Data Engineering: ETL pipelines, data modeling
- Big Data: Apache Spark, distributed computing
- Analytics: Statistical analysis, visualization
- SQL: Query optimization, database design
- Python: Data processing, automation

## 🎯 Next Steps

Potential enhancements:
- [ ] Add machine learning models for sales prediction
- [ ] Create interactive dashboards (Streamlit/Dash)
- [ ] Implement real-time data processing
- [ ] Add data lineage tracking
- [ ] Create automated reports
- [ ] Deploy to cloud platform (AWS/Azure/GCP)
- [ ] Add CI/CD pipeline
- [ ] Implement data versioning

## 📞 Contact

For questions or feedback, please open an issue in this repository.

---

**Dataset Credit**: [Ahmed Mohamed Ibrahim](https://www.kaggle.com/ahmedmohamedibrahim1) - Coffee Shop Sales Dataset on Kaggle
