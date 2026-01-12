"""
Simple tests for the ETL pipeline scripts.
Run with: pytest tests/test_pipeline.py
"""

import pytest
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


def test_project_structure():
    """Test that required directories exist"""
    base_path = Path(__file__).parent.parent
    
    required_dirs = [
        "data/raw",
        "data/cleaned",
        "data/processed",
        "scripts",
        "notebooks",
        "sql",
        "config"
    ]
    
    for dir_path in required_dirs:
        full_path = base_path / dir_path
        assert full_path.exists(), f"Directory {dir_path} does not exist"


def test_config_file_exists():
    """Test that configuration file exists"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    assert config_path.exists(), "config.yaml does not exist"


def test_requirements_file():
    """Test that requirements.txt exists and has content"""
    req_path = Path(__file__).parent.parent / "requirements.txt"
    assert req_path.exists(), "requirements.txt does not exist"
    
    content = req_path.read_text()
    assert len(content) > 0, "requirements.txt is empty"
    assert "pandas" in content, "pandas not in requirements"
    assert "pyspark" in content, "pyspark not in requirements"


def test_scripts_exist():
    """Test that all main scripts exist"""
    base_path = Path(__file__).parent.parent / "scripts"
    
    required_scripts = [
        "01_extract.py",
        "02_transform.py",
        "03_load.py",
        "spark_processing.py",
        "data_quality_check.py"
    ]
    
    for script in required_scripts:
        script_path = base_path / script
        assert script_path.exists(), f"Script {script} does not exist"


def test_sql_files_exist():
    """Test that SQL files exist"""
    base_path = Path(__file__).parent.parent / "sql"
    
    required_files = [
        "schema.sql",
        "analytics_queries.sql"
    ]
    
    for file_name in required_files:
        file_path = base_path / file_name
        assert file_path.exists(), f"SQL file {file_name} does not exist"


def test_notebooks_exist():
    """Test that Jupyter notebooks exist"""
    base_path = Path(__file__).parent.parent / "notebooks"
    
    required_notebooks = [
        "01_exploratory_data_analysis.ipynb",
        "02_spark_analysis.ipynb"
    ]
    
    for notebook in required_notebooks:
        notebook_path = base_path / notebook
        assert notebook_path.exists(), f"Notebook {notebook} does not exist"


def test_import_extract_module():
    """Test that extract module can be imported"""
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from scripts import extract as extract_module
        assert hasattr(extract_module, 'load_config')
    except ImportError:
        pytest.skip("Module import test skipped - dependencies may not be installed")


def test_gitignore_exists():
    """Test that .gitignore exists"""
    gitignore_path = Path(__file__).parent.parent / ".gitignore"
    assert gitignore_path.exists(), ".gitignore does not exist"
    
    content = gitignore_path.read_text()
    assert "__pycache__" in content, "__pycache__ not in .gitignore"
    assert ".ipynb_checkpoints" in content, ".ipynb_checkpoints not in .gitignore"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
