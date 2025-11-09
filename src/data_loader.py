"""
Data Loading Module

This module provides functions for loading and preprocessing solar energy datasets.
Supports loading data from CSV files with automatic path resolution and basic validation.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Optional, Tuple


def get_data_path(filename: str, data_dir: str = "data") -> Path:
    """
    Get the absolute path to a data file.
    
    Parameters:
    -----------
    filename : str
        Name of the data file (e.g., 'benin-malanville.csv')
    data_dir : str, default='data'
        Name of the data directory relative to project root
    
    Returns:
    --------
    Path
        Absolute path to the data file
    """
    # Get project root (assuming this file is in src/)
    project_root = Path(__file__).parent.parent
    data_path = project_root / data_dir / filename
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    return data_path


def load_solar_data(filename: str, data_dir: str = "data", 
                   parse_dates: Optional[list] = None) -> pd.DataFrame:
    """
    Load solar energy dataset from CSV file.
    
    Parameters:
    -----------
    filename : str
        Name of the CSV file to load
    data_dir : str, default='data'
        Directory containing the data files
    parse_dates : list, optional
        List of column names to parse as dates
    
    Returns:
    --------
    pd.DataFrame
        Loaded dataset as a pandas DataFrame
    
    Examples:
    ---------
    >>> df = load_solar_data('benin-malanville.csv')
    >>> df = load_solar_data('togo-dapaong_qc.csv', parse_dates=['Timestamp'])
    """
    filepath = get_data_path(filename, data_dir)
    
    # Default to parsing 'Timestamp' if it exists
    if parse_dates is None:
        df_sample = pd.read_csv(filepath, nrows=1)
        if 'Timestamp' in df_sample.columns:
            parse_dates = ['Timestamp']
    
    df = pd.read_csv(filepath, parse_dates=parse_dates)
    
    print(f"✓ Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def get_dataset_info() -> dict:
    """
    Get information about available datasets.
    
    Returns:
    --------
    dict
        Dictionary mapping dataset names to their file paths
    """
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    
    datasets = {}
    if data_dir.exists():
        for file in data_dir.glob("*.csv"):
            # Skip cleaned datasets
            if "clean" not in file.stem:
                datasets[file.stem] = str(file.name)
    
    return datasets

