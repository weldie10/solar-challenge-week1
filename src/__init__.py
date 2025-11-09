"""
Solar Challenge Week 1 - Source Package

This package contains modular utilities for data loading, profiling, and EDA.
"""

from .data_loader import load_solar_data, get_data_path, get_dataset_info
from .data_profiler import (
    profile_missing_values,
    generate_summary_statistics,
    detect_outliers_zscore,
    get_data_quality_report,
    clean_data
)
from .eda_utils import (
    plot_correlation_heatmap,
    plot_time_series,
    plot_distributions,
    plot_scatter_matrix,
    save_cleaned_data
)

__version__ = "1.0.0"
__all__ = [
    # Data loading
    'load_solar_data',
    'get_data_path',
    'get_dataset_info',
    # Data profiling
    'profile_missing_values',
    'generate_summary_statistics',
    'detect_outliers_zscore',
    'get_data_quality_report',
    'clean_data',
    # EDA utilities
    'plot_correlation_heatmap',
    'plot_time_series',
    'plot_distributions',
    'plot_scatter_matrix',
    'save_cleaned_data',
]

