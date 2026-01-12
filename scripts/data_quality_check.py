"""
Data Quality Checks for Coffee Sales Dataset
This script performs data quality validation and profiling.
"""

import pandas as pd
from pathlib import Path
import yaml
from datetime import datetime


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_data(data_path):
    """Load data for quality checks"""
    parquet_files = list(data_path.glob("*.parquet"))
    
    if parquet_files:
        latest_file = max(parquet_files, key=lambda x: x.stat().st_mtime)
        print(f"Loading data from: {latest_file.name}")
        df = pd.read_parquet(latest_file)
    else:
        csv_files = list(data_path.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"No data files found in {data_path}")
        
        latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
        print(f"Loading data from: {latest_file.name}")
        df = pd.read_csv(latest_file)
    
    return df


def check_completeness(df):
    """Check data completeness"""
    print("\n" + "=" * 50)
    print("Data Completeness Check")
    print("=" * 50)
    
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    completeness = (1 - missing_cells / total_cells) * 100
    
    print(f"\nTotal cells: {total_cells:,}")
    print(f"Missing cells: {missing_cells:,}")
    print(f"Completeness: {completeness:.2f}%")
    
    print("\nMissing values per column:")
    missing_per_column = df.isnull().sum()
    missing_pct = (missing_per_column / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': missing_per_column.index,
        'Missing_Count': missing_per_column.values,
        'Missing_Percentage': missing_pct.values
    })
    
    print(missing_df[missing_df['Missing_Count'] > 0].to_string(index=False))
    
    return completeness >= 95  # Pass if 95% or more complete


def check_uniqueness(df):
    """Check for duplicates"""
    print("\n" + "=" * 50)
    print("Uniqueness Check")
    print("=" * 50)
    
    total_rows = len(df)
    duplicate_rows = df.duplicated().sum()
    uniqueness = (1 - duplicate_rows / total_rows) * 100
    
    print(f"\nTotal rows: {total_rows:,}")
    print(f"Duplicate rows: {duplicate_rows:,}")
    print(f"Uniqueness: {uniqueness:.2f}%")
    
    return duplicate_rows == 0


def check_validity(df):
    """Check data validity (data types, ranges)"""
    print("\n" + "=" * 50)
    print("Validity Check")
    print("=" * 50)
    
    print("\nData Types:")
    print(df.dtypes.to_string())
    
    # Check for negative values in numeric columns (if they shouldn't be negative)
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    print("\nNumeric Column Ranges:")
    for col in numeric_cols:
        min_val = df[col].min()
        max_val = df[col].max()
        print(f"{col}: [{min_val}, {max_val}]")
        
        # Flag if any numeric values are negative (adjust logic based on domain)
        if min_val < 0:
            print(f"  ⚠ Warning: {col} contains negative values")
    
    return True


def check_consistency(df):
    """Check data consistency"""
    print("\n" + "=" * 50)
    print("Consistency Check")
    print("=" * 50)
    
    # Check for consistent formatting in categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    print("\nCategorical Column Cardinality:")
    for col in categorical_cols[:5]:  # Limit to first 5
        unique_count = df[col].nunique()
        print(f"{col}: {unique_count} unique values")
    
    return True


def data_profiling(df):
    """Generate data profile report"""
    print("\n" + "=" * 50)
    print("Data Profiling")
    print("=" * 50)
    
    print(f"\nDataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print("\nColumn Summary:")
    for col in df.columns:
        dtype = df[col].dtype
        unique = df[col].nunique()
        missing = df[col].isnull().sum()
        print(f"  {col}: {dtype}, {unique} unique, {missing} missing")


def generate_quality_report(results):
    """Generate quality check report"""
    print("\n" + "=" * 50)
    print("Data Quality Report")
    print("=" * 50)
    
    all_passed = all(results.values())
    
    print("\nCheck Results:")
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {check}: {status}")
    
    print(f"\nOverall Status: {'✓ ALL CHECKS PASSED' if all_passed else '✗ SOME CHECKS FAILED'}")
    
    return all_passed


def main():
    """Main quality check pipeline"""
    print("Coffee Sales Data Quality Checks")
    print("=" * 50)
    
    config = load_config()
    project_root = Path(__file__).parent.parent
    
    # Check both cleaned and processed data
    cleaned_path = project_root / config['data']['cleaned_data_path']
    
    try:
        # Load data
        df = load_data(cleaned_path)
        
        # Perform data profiling
        data_profiling(df)
        
        # Perform quality checks
        results = {
            'Completeness': check_completeness(df),
            'Uniqueness': check_uniqueness(df),
            'Validity': check_validity(df),
            'Consistency': check_consistency(df)
        }
        
        # Generate report
        all_passed = generate_quality_report(results)
        
        print("\n" + "=" * 50)
        
        if not all_passed:
            print("⚠ Warning: Some quality checks failed. Review the data.")
        else:
            print("✓ All quality checks passed!")
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please run the ETL pipeline first.")
    except Exception as e:
        print(f"\nError during quality checks: {e}")
        raise


if __name__ == "__main__":
    main()
