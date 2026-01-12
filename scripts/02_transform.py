"""
Data Transformation Script for Coffee Sales Dataset
This script cleans, transforms, and prepares the data for analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import yaml
from datetime import datetime


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_raw_data(raw_data_path):
    """Load raw data from CSV or Excel files"""
    csv_files = list(raw_data_path.glob("*.csv"))
    
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {raw_data_path}")
    
    # Load the first CSV file (adjust based on actual dataset structure)
    data_file = csv_files[0]
    print(f"Loading data from: {data_file.name}")
    
    df = pd.read_csv(data_file)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    return df


def clean_data(df):
    """Clean and preprocess the data"""
    print("\nCleaning data...")
    
    # Make a copy to avoid modifying original
    df_clean = df.copy()
    
    # Remove duplicates
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    print(f"Removed {initial_rows - len(df_clean)} duplicate rows")
    
    # Handle missing values
    missing_before = df_clean.isnull().sum().sum()
    
    # Fill numeric columns with median
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_clean[col].isnull().any():
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    
    # Fill categorical columns with mode or 'Unknown'
    categorical_cols = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df_clean[col].isnull().any():
            mode_val = df_clean[col].mode()
            if len(mode_val) > 0:
                df_clean[col] = df_clean[col].fillna(mode_val[0])
            else:
                df_clean[col] = df_clean[col].fillna('Unknown')
    
    missing_after = df_clean.isnull().sum().sum()
    print(f"Handled {missing_before - missing_after} missing values")
    
    return df_clean


def transform_data(df):
    """Transform data for analysis"""
    print("\nTransforming data...")
    
    df_transform = df.copy()
    
    # Parse date columns (adjust column names based on actual dataset)
    date_columns = [col for col in df_transform.columns if 'date' in col.lower() or 'time' in col.lower()]
    
    for col in date_columns:
        try:
            df_transform[col] = pd.to_datetime(df_transform[col])
            print(f"Parsed datetime column: {col}")
        except Exception as e:
            print(f"Could not parse {col} as datetime: {e}")
    
    # Create additional time-based features if date columns exist
    for col in date_columns:
        if pd.api.types.is_datetime64_any_dtype(df_transform[col]):
            df_transform[f'{col}_year'] = df_transform[col].dt.year
            df_transform[f'{col}_month'] = df_transform[col].dt.month
            df_transform[f'{col}_day'] = df_transform[col].dt.day
            df_transform[f'{col}_dayofweek'] = df_transform[col].dt.dayofweek
            df_transform[f'{col}_hour'] = df_transform[col].dt.hour
            print(f"Created time features from {col}")
    
    return df_transform


def save_cleaned_data(df, cleaned_data_path):
    """Save cleaned data"""
    cleaned_data_path.mkdir(parents=True, exist_ok=True)
    
    # Save as CSV
    csv_file = cleaned_data_path / f"coffee_sales_cleaned_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(csv_file, index=False)
    print(f"\nSaved cleaned data to: {csv_file}")
    
    # Save as Parquet for better performance with big data
    parquet_file = cleaned_data_path / f"coffee_sales_cleaned_{datetime.now().strftime('%Y%m%d')}.parquet"
    df.to_parquet(parquet_file, index=False)
    print(f"Saved cleaned data to: {parquet_file}")


def main():
    """Main transformation pipeline"""
    print("Coffee Sales Data Transformation")
    print("=" * 50)
    
    config = load_config()
    project_root = Path(__file__).parent.parent
    raw_data_path = project_root / config['data']['raw_data_path']
    cleaned_data_path = project_root / config['data']['cleaned_data_path']
    
    try:
        # Load raw data
        df = load_raw_data(raw_data_path)
        
        # Display basic info
        print("\nDataset Overview:")
        print(df.head())
        print("\nColumn Types:")
        print(df.dtypes)
        print("\nBasic Statistics:")
        print(df.describe())
        
        # Clean data
        df_clean = clean_data(df)
        
        # Transform data
        df_final = transform_data(df_clean)
        
        # Save cleaned data
        save_cleaned_data(df_final, cleaned_data_path)
        
        print("\n" + "=" * 50)
        print("Transformation completed successfully!")
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please run 01_extract.py first to download the dataset.")
    except Exception as e:
        print(f"\nError during transformation: {e}")
        raise


if __name__ == "__main__":
    main()
