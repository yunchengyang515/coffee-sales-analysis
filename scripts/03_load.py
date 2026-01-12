"""
Data Loading Script for Coffee Sales Dataset
This script loads processed data into a database or data warehouse.
"""

import pandas as pd
from pathlib import Path
import yaml
from sqlalchemy import create_engine, text
from datetime import datetime


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_database_connection(config):
    """Create database connection using SQLAlchemy"""
    import os
    db_config = config['database']
    
    # Use environment variables for credentials if available, otherwise fall back to config
    db_user = os.getenv('DB_USER', db_config['user'])
    db_password = os.getenv('DB_PASSWORD', db_config['password'])
    db_host = os.getenv('DB_HOST', db_config['host'])
    db_port = os.getenv('DB_PORT', db_config['port'])
    db_name = os.getenv('DB_NAME', db_config['database'])
    
    # Example for PostgreSQL
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    try:
        engine = create_engine(connection_string)
        print("Database connection established successfully")
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("Please update database credentials in config/config.yaml")
        return None


def load_cleaned_data(cleaned_data_path):
    """Load cleaned data from parquet or CSV"""
    # Try to load parquet first (more efficient)
    parquet_files = list(cleaned_data_path.glob("*.parquet"))
    
    if parquet_files:
        latest_file = max(parquet_files, key=lambda x: x.stat().st_mtime)
        print(f"Loading data from: {latest_file.name}")
        df = pd.read_parquet(latest_file)
    else:
        # Fall back to CSV
        csv_files = list(cleaned_data_path.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"No data files found in {cleaned_data_path}")
        
        latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
        print(f"Loading data from: {latest_file.name}")
        df = pd.read_csv(latest_file)
    
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    return df


def load_to_database(df, engine, table_name='coffee_sales'):
    """Load data into database"""
    if engine is None:
        print("Skipping database load - no connection available")
        return
    
    print(f"\nLoading data to table: {table_name}")
    
    try:
        # Load data to database
        df.to_sql(
            table_name,
            engine,
            if_exists='replace',  # Options: 'fail', 'replace', 'append'
            index=False,
            chunksize=1000
        )
        print(f"Successfully loaded {len(df)} rows to {table_name}")
        
        # Verify the load
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            print(f"Verified: {count} rows in database table")
            
    except Exception as e:
        print(f"Error loading data to database: {e}")
        raise


def save_to_processed(df, processed_data_path):
    """Save processed data to processed directory"""
    processed_data_path.mkdir(parents=True, exist_ok=True)
    
    # Save as Parquet with partitioning for big data scenarios
    parquet_file = processed_data_path / f"coffee_sales_processed_{datetime.now().strftime('%Y%m%d')}.parquet"
    df.to_parquet(parquet_file, index=False, engine='pyarrow', compression='snappy')
    print(f"\nSaved processed data to: {parquet_file}")


def main():
    """Main loading pipeline"""
    print("Coffee Sales Data Loading")
    print("=" * 50)
    
    config = load_config()
    project_root = Path(__file__).parent.parent
    cleaned_data_path = project_root / config['data']['cleaned_data_path']
    processed_data_path = project_root / config['data']['processed_data_path']
    
    try:
        # Load cleaned data
        df = load_cleaned_data(cleaned_data_path)
        
        # Save to processed directory
        save_to_processed(df, processed_data_path)
        
        # Create database connection (optional)
        engine = create_database_connection(config)
        
        # Load to database if connection is available
        if engine:
            load_to_database(df, engine)
        
        print("\n" + "=" * 50)
        print("Loading completed successfully!")
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please run 02_transform.py first to clean the dataset.")
    except Exception as e:
        print(f"\nError during loading: {e}")
        raise


if __name__ == "__main__":
    main()
