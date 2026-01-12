# Raw Data Directory

This directory should contain the raw data downloaded from Kaggle.

## How to Download

### Using Kaggle CLI:
```bash
kaggle datasets download -d ahmedmohamedibrahim1/coffee-shop-sales-dataset -p data/raw/ --unzip
```

### Manual Download:
1. Visit: https://www.kaggle.com/datasets/ahmedmohamedibrahim1/coffee-shop-sales-dataset
2. Click "Download"
3. Extract files to this directory

## Expected Files

After downloading, this directory should contain:
- CSV or Excel files with coffee sales data
- Any additional documentation from Kaggle

## Note

Raw data files are excluded from git (see `.gitignore`) to keep the repository size small.
