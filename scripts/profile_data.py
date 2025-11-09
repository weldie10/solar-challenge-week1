#!/usr/bin/env python3
"""
Data Profiling Script

This script performs comprehensive data profiling on solar energy datasets.
It generates reports on missing values, outliers, data quality, and summary statistics.

Usage:
    python scripts/profile_data.py <dataset_name>
    
Examples:
    python scripts/profile_data.py benin-malanville
    python scripts/profile_data.py togo-dapaong_qc
    python scripts/profile_data.py sierraleone-bumbuna
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

import pandas as pd
from data_loader import load_solar_data, get_dataset_info
from data_profiler import (
    profile_missing_values,
    generate_summary_statistics,
    detect_outliers_zscore,
    get_data_quality_report
)


def main():
    """Main function to run data profiling."""
    # Get available datasets
    datasets = get_dataset_info()
    
    if len(sys.argv) < 2:
        print("Available datasets:")
        for name, filename in datasets.items():
            print(f"  - {name}: {filename}")
        print("\nUsage: python scripts/profile_data.py <dataset_name>")
        print("Example: python scripts/profile_data.py benin-malanville")
        return
    
    dataset_name = sys.argv[1]
    
    # Find matching dataset
    filename = None
    for name, fname in datasets.items():
        if dataset_name.lower() in name.lower():
            filename = fname
            break
    
    if filename is None:
        print(f"Error: Dataset '{dataset_name}' not found.")
        print("Available datasets:", list(datasets.keys()))
        return
    
    print(f"\n{'='*60}")
    print(f"Profiling Dataset: {filename}")
    print(f"{'='*60}\n")
    
    # Load data
    try:
        df = load_solar_data(filename, parse_dates=['Timestamp'] if 'Timestamp' in pd.read_csv(
            project_root / "data" / filename, nrows=1).columns else None)
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Generate profiling reports
    print("\n1. DATA QUALITY REPORT")
    print("-" * 60)
    quality_report = get_data_quality_report(df)
    print(f"Shape: {quality_report['shape']}")
    print(f"Memory Usage: {quality_report['memory_usage_mb']:.2f} MB")
    print(f"Duplicate Rows: {quality_report['duplicate_rows']}")
    
    print("\n2. MISSING VALUES ANALYSIS")
    print("-" * 60)
    missing_df = profile_missing_values(df)
    print(missing_df.to_string(index=False))
    
    high_missing = missing_df[missing_df['High_Missing'] == True]
    if len(high_missing) > 0:
        print(f"\n⚠️  Warning: {len(high_missing)} columns have >5% missing values")
        print(high_missing[['Column', 'Missing_Percentage']].to_string(index=False))
    
    print("\n3. SUMMARY STATISTICS")
    print("-" * 60)
    summary = generate_summary_statistics(df)
    print(summary)
    
    print("\n4. OUTLIER DETECTION")
    print("-" * 60)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    # Use key columns for outlier detection
    key_cols = [col for col in ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust'] 
                if col in numeric_cols]
    if not key_cols:
        key_cols = numeric_cols[:7]  # Use first 7 numeric columns
    
    outlier_info = detect_outliers_zscore(df, key_cols, threshold=3.0)
    print(f"Outliers detected: {outlier_info['outlier_count']} rows")
    print(f"Percentage: {outlier_info['outlier_count'] / len(df) * 100:.2f}%")
    print(f"Columns analyzed: {', '.join(key_cols)}")
    
    print("\n5. DATA TYPES")
    print("-" * 60)
    dtype_summary = pd.DataFrame({
        'Column': df.columns,
        'DataType': df.dtypes,
        'Non-Null Count': df.count(),
        'Null Count': df.isnull().sum()
    })
    print(dtype_summary.to_string(index=False))
    
    print(f"\n{'='*60}")
    print("Profiling complete!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

