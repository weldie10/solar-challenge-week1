"""
Data Profiling Module

This module provides comprehensive data profiling functions for exploratory data analysis.
Includes functions for missing value analysis, statistical summaries, and data quality checks.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from scipy import stats


def profile_missing_values(df: pd.DataFrame, threshold: float = 0.05) -> pd.DataFrame:
    """
    Profile missing values in the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    threshold : float, default=0.05
        Threshold for flagging columns with high missing percentage
    
    Returns:
    --------
    pd.DataFrame
        Summary of missing values with counts and percentages
    """
    missing = df.isna().sum()
    missing_pct = (missing / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing_Count': missing.values,
        'Missing_Percentage': missing_pct.values,
        'High_Missing': missing_pct.values > (threshold * 100)
    }).sort_values('Missing_Percentage', ascending=False)
    
    return missing_df


def generate_summary_statistics(df: pd.DataFrame, 
                               include_all: bool = False) -> pd.DataFrame:
    """
    Generate comprehensive summary statistics for numeric columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    include_all : bool, default=False
        If True, include non-numeric columns in summary
    
    Returns:
    --------
    pd.DataFrame
        Summary statistics for each numeric column
    """
    return df.describe(include='all' if include_all else None)


def detect_outliers_zscore(df: pd.DataFrame, 
                           columns: Optional[List[str]] = None,
                           threshold: float = 3.0) -> Dict:
    """
    Detect outliers using Z-score method.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list, optional
        List of column names to check. If None, uses all numeric columns.
    threshold : float, default=3.0
        Z-score threshold for outlier detection
    
    Returns:
    --------
    dict
        Dictionary containing:
        - 'outlier_mask': Boolean array indicating outliers
        - 'outlier_count': Number of outliers per column
        - 'outlier_rows': DataFrame with outlier rows
        - 'z_scores': Z-scores for each column
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    z_scores = np.abs(stats.zscore(df[columns], nan_policy='omit'))
    outlier_mask = (z_scores > threshold).any(axis=1)
    
    result = {
        'outlier_mask': outlier_mask,
        'outlier_count': outlier_mask.sum(),
        'outlier_rows': df[outlier_mask],
        'z_scores': pd.DataFrame(z_scores, columns=columns, index=df.index),
        'columns_analyzed': columns
    }
    
    return result


def get_data_quality_report(df: pd.DataFrame) -> Dict:
    """
    Generate a comprehensive data quality report.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    
    Returns:
    --------
    dict
        Dictionary containing data quality metrics
    """
    report = {
        'shape': df.shape,
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'dtypes': df.dtypes.to_dict(),
        'missing_values': profile_missing_values(df).to_dict('records'),
        'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
        'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
        'duplicate_rows': df.duplicated().sum()
    }
    
    return report


def clean_data(df: pd.DataFrame, 
              numeric_cols: Optional[List[str]] = None,
              outlier_threshold: float = 3.0,
              fill_method: str = 'median') -> pd.DataFrame:
    """
    Clean dataset by handling missing values and outliers.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    numeric_cols : list, optional
        Numeric columns to clean. If None, auto-detects.
    outlier_threshold : float, default=3.0
        Z-score threshold for outlier removal
    fill_method : str, default='median'
        Method for filling missing values ('median', 'mean', 'mode')
    
    Returns:
    --------
    pd.DataFrame
        Cleaned dataframe
    """
    df_clean = df.copy()
    
    if numeric_cols is None:
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    
    # Handle missing values
    if fill_method == 'median':
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(
            df_clean[numeric_cols].median()
        )
    elif fill_method == 'mean':
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(
            df_clean[numeric_cols].mean()
        )
    
    # Remove outliers
    outlier_info = detect_outliers_zscore(df_clean, numeric_cols, outlier_threshold)
    df_clean = df_clean[~outlier_info['outlier_mask']]
    
    print(f"✓ Cleaned dataset: {df_clean.shape[0]} rows (removed {outlier_info['outlier_count']} outliers)")
    
    return df_clean

