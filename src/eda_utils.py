"""
Exploratory Data Analysis Utilities

This module provides visualization and analysis functions for EDA.
Includes functions for correlation analysis, time series plotting, and distribution analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional
from pathlib import Path
import os


def plot_correlation_heatmap(df: pd.DataFrame, 
                             columns: Optional[List[str]] = None,
                             figsize: tuple = (10, 8),
                             save_path: Optional[str] = None) -> None:
    """
    Plot correlation heatmap for numeric columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list, optional
        Columns to include in correlation. If None, uses all numeric columns.
    figsize : tuple, default=(10, 8)
        Figure size
    save_path : str, optional
        Path to save the figure
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    plt.figure(figsize=figsize)
    corr_matrix = df[columns].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0,
                square=True, fmt='.2f', cbar_kws={"shrink": 0.8})
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_time_series(df: pd.DataFrame,
                    time_col: str,
                    value_cols: List[str],
                    figsize: tuple = (12, 6),
                    save_path: Optional[str] = None) -> None:
    """
    Plot time series for specified columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    time_col : str
        Name of the time column
    value_cols : list
        List of column names to plot
    figsize : tuple, default=(12, 6)
        Figure size
    save_path : str, optional
        Path to save the figure
    """
    plt.figure(figsize=figsize)
    
    for col in value_cols:
        plt.plot(df[time_col], df[col], label=col, alpha=0.7)
    
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Time Series Analysis")
    plt.legend(loc="upper right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_distributions(df: pd.DataFrame,
                      columns: List[str],
                      bins: int = 30,
                      figsize: tuple = (15, 5),
                      save_path: Optional[str] = None) -> None:
    """
    Plot distributions for multiple columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list
        List of column names to plot
    bins : int, default=30
        Number of bins for histograms
    figsize : tuple, default=(15, 5)
        Figure size
    save_path : str, optional
        Path to save the figure
    """
    n_cols = len(columns)
    n_rows = (n_cols + 2) // 3
    
    fig, axes = plt.subplots(n_rows, 3, figsize=figsize)
    axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes
    
    for idx, col in enumerate(columns):
        sns.histplot(df[col], bins=bins, kde=True, ax=axes[idx])
        axes[idx].set_title(f"{col} Distribution")
        axes[idx].grid(True, alpha=0.3)
    
    # Hide unused subplots
    for idx in range(len(columns), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_scatter_matrix(df: pd.DataFrame,
                       columns: List[str],
                       hue: Optional[str] = None,
                       figsize: tuple = (12, 10),
                       save_path: Optional[str] = None) -> None:
    """
    Create scatter plot matrix for selected columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list
        List of column names to include
    hue : str, optional
        Column name for color coding
    figsize : tuple, default=(12, 10)
        Figure size
    save_path : str, optional
        Path to save the figure
    """
    plt.figure(figsize=figsize)
    
    if hue:
        sns.pairplot(df[columns + [hue]], hue=hue, diag_kind='kde')
    else:
        sns.pairplot(df[columns], diag_kind='kde')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def save_cleaned_data(df: pd.DataFrame, 
                     filename: str,
                     output_dir: str = "data") -> str:
    """
    Save cleaned dataframe to CSV.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe to save
    filename : str
        Output filename (will add '_clean' suffix if not present)
    output_dir : str, default='data'
        Output directory
    
    Returns:
    --------
    str
        Path to saved file
    """
    project_root = Path(__file__).parent.parent
    output_path = project_root / output_dir
    
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
    
    if '_clean' not in filename:
        base_name = filename.replace('.csv', '')
        filename = f"{base_name}_clean.csv"
    
    filepath = output_path / filename
    df.to_csv(filepath, index=False)
    
    print(f"✓ Saved cleaned data to: {filepath}")
    return str(filepath)

