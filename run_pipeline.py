"""
Run the complete ETL pipeline.
Execute all ETL scripts in sequence.
"""

import subprocess
import sys
from pathlib import Path


def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print("\n" + "=" * 70)
    print(f"Running: {description}")
    print("=" * 70)
    
    script_path = Path(__file__).parent / "scripts" / script_name
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False
        )
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"✗ Error running {description}: {e}")
        return False


def main():
    """Run the complete pipeline"""
    print("\n" + "=" * 70)
    print("Coffee Sales Analysis - Complete ETL Pipeline")
    print("=" * 70)
    
    pipeline_steps = [
        ("01_extract.py", "Data Extraction"),
        ("02_transform.py", "Data Transformation"),
        ("03_load.py", "Data Loading"),
        ("data_quality_check.py", "Data Quality Checks"),
    ]
    
    results = {}
    
    for script, description in pipeline_steps:
        success = run_script(script, description)
        results[description] = success
        
        if not success and script != "01_extract.py":
            # Continue even if extraction fails (data might already exist)
            # But stop if other steps fail
            print(f"\n⚠ Pipeline stopped due to failure in {description}")
            break
    
    # Print summary
    print("\n" + "=" * 70)
    print("Pipeline Execution Summary")
    print("=" * 70)
    
    for step, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {step}")
    
    all_success = all(results.values())
    
    print("\n" + "=" * 70)
    if all_success:
        print("✓ Pipeline completed successfully!")
        print("\nNext steps:")
        print("1. Run Spark processing: python scripts/spark_processing.py")
        print("2. Open Jupyter notebooks for analysis")
        print("3. Run SQL queries from sql/ directory")
    else:
        print("⚠ Pipeline completed with errors. Please check the logs above.")
    print("=" * 70)


if __name__ == "__main__":
    main()
