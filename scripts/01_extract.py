"""
Data Extraction Script for Coffee Sales Dataset
This script downloads and extracts data from the Kaggle dataset.
"""

import os
import yaml
from pathlib import Path


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def download_dataset():
    """
    Download the Coffee Sales dataset from Kaggle.
    
    Prerequisites:
    - Kaggle API credentials configured (~/.kaggle/kaggle.json)
    - Install kaggle package: pip install kaggle
    
    Run: kaggle datasets download -d ahmedmohamedibrahim1/coffee-shop-sales-dataset
    """
    config = load_config()
    dataset_name = config['data']['kaggle_dataset']
    raw_data_path = Path(__file__).parent.parent / config['data']['raw_data_path']
    
    print(f"Dataset: {dataset_name}")
    print(f"Download location: {raw_data_path}")
    print("\nTo download the dataset, run the following command:")
    print(f"kaggle datasets download -d {dataset_name} -p {raw_data_path} --unzip")
    print("\nNote: Ensure you have Kaggle API credentials set up.")


def extract_data():
    """Extract data from downloaded files"""
    config = load_config()
    raw_data_path = Path(__file__).parent.parent / config['data']['raw_data_path']
    
    if not raw_data_path.exists():
        print(f"Raw data directory not found: {raw_data_path}")
        return
    
    csv_files = list(raw_data_path.glob("*.csv"))
    excel_files = list(raw_data_path.glob("*.xlsx"))
    
    print(f"\nFound {len(csv_files)} CSV files")
    print(f"Found {len(excel_files)} Excel files")
    
    for file in csv_files + excel_files:
        print(f"  - {file.name}")


if __name__ == "__main__":
    print("Coffee Sales Data Extraction")
    print("=" * 50)
    download_dataset()
    print("\n" + "=" * 50)
    extract_data()
