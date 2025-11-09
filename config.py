"""
Configuration file for Solar Challenge Week 1 project.

This module contains project-wide configuration settings.
"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
RESULTS_DIR = PROJECT_ROOT / "results"
SRC_DIR = PROJECT_ROOT / "src"

# Data processing settings
OUTLIER_THRESHOLD = 3.0  # Z-score threshold for outlier detection
MISSING_VALUE_THRESHOLD = 0.05  # 5% threshold for flagging high missing values
FILL_METHOD = 'median'  # Method for filling missing values: 'median', 'mean', or 'mode'

# Visualization settings
FIGURE_SIZE = (12, 6)
DPI = 300
COLOR_PALETTE = "coolwarm"

# Key columns for analysis
IRRADIANCE_COLS = ['GHI', 'DNI', 'DHI']
MODULE_COLS = ['ModA', 'ModB']
TEMPERATURE_COLS = ['Tamb', 'TModA', 'TModB']
WEATHER_COLS = ['WS', 'WSgust', 'WD', 'RH', 'BP', 'Precipitation']

# Dataset names
DATASETS = {
    'benin': 'benin-malanville.csv',
    'sierraleone': 'sierraleone-bumbuna.csv',
    'togo': 'togo-dapaong_qc.csv'
}

