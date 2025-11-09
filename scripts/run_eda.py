#!/usr/bin/env python3
"""
Exploratory Data Analysis Script

This script performs comprehensive EDA on solar energy datasets.
It generates visualizations including correlation heatmaps, time series plots,
distributions, and saves cleaned datasets.

Usage:
    python scripts/run_eda.py <dataset_name> [--output-dir OUTPUT_DIR]
    
Examples:
    python scripts/run_eda.py benin-malanville
    python scripts/run_eda.py togo-dapaong_qc --output-dir results
"""

import sys
import argparse
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

import pandas as pd
import numpy as np
from data_loader import load_solar_data, get_dataset_info
from data_profiler import clean_data, detect_outliers_zscore
from eda_utils import (
    plot_correlation_heatmap,
    plot_time_series,
    plot_distributions,
    save_cleaned_data
)


def main():
    """Main function to run EDA."""
    parser = argparse.ArgumentParser(description='Run EDA on solar energy datasets')
    parser.add_argument('dataset', help='Dataset name (e.g., benin-malanville)')
    parser.add_argument('--output-dir', default='results', 
                       help='Output directory for plots and cleaned data')
    parser.add_argument('--skip-cleaning', action='store_true',
                       help='Skip data cleaning step')
    
    args = parser.parse_args()
    
    # Get available datasets
    datasets = get_dataset_info()
    
    # Find matching dataset
    filename = None
    for name, fname in datasets.items():
        if args.dataset.lower() in name.lower():
            filename = fname
            break
    
    if filename is None:
        print(f"Error: Dataset '{args.dataset}' not found.")
        print("Available datasets:", list(datasets.keys()))
        return
    
    print(f"\n{'='*60}")
    print(f"Running EDA on: {filename}")
    print(f"{'='*60}\n")
    
    # Create output directory
    output_dir = project_root / args.output_dir
    output_dir.mkdir(exist_ok=True)
    
    # Load data
    try:
        df = load_solar_data(filename, parse_dates=['Timestamp'] if 'Timestamp' in pd.read_csv(
            project_root / "data" / filename, nrows=1).columns else None)
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Clean data if requested
    if not args.skip_cleaning:
        print("\nCleaning data...")
        numeric_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
        numeric_cols = [col for col in numeric_cols if col in df.columns]
        
        df_clean = clean_data(df, numeric_cols=numeric_cols, outlier_threshold=3.0)
        
        # Save cleaned data
        clean_filename = filename.replace('.csv', '_clean.csv')
        save_cleaned_data(df_clean, clean_filename)
    else:
        df_clean = df.copy()
        print("Skipping data cleaning...")
    
    # Prepare columns for analysis
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    
    # 1. Correlation Analysis
    print("\n1. Generating correlation heatmap...")
    key_cols = [col for col in ['GHI', 'DNI', 'DHI', 'TModA', 'TModB'] 
                if col in numeric_cols]
    if key_cols:
        plot_correlation_heatmap(
            df_clean, 
            columns=key_cols,
            save_path=str(output_dir / f"{args.dataset}_correlation.png")
        )
    
    # 2. Time Series Analysis
    if 'Timestamp' in df_clean.columns:
        print("\n2. Generating time series plots...")
        irradiance_cols = [col for col in ['GHI', 'DNI', 'DHI'] 
                          if col in df_clean.columns]
        if irradiance_cols:
            plot_time_series(
                df_clean,
                time_col='Timestamp',
                value_cols=irradiance_cols,
                save_path=str(output_dir / f"{args.dataset}_timeseries.png")
            )
    
    # 3. Distribution Analysis
    print("\n3. Generating distribution plots...")
    dist_cols = [col for col in ['GHI', 'WS', 'Tamb', 'RH'] 
                 if col in numeric_cols][:6]
    if dist_cols:
        plot_distributions(
            df_clean,
            columns=dist_cols,
            save_path=str(output_dir / f"{args.dataset}_distributions.png")
        )
    
    print(f"\n{'='*60}")
    print(f"EDA complete! Results saved to: {output_dir}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

